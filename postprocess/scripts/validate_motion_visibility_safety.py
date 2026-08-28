#!/usr/bin/env python3
"""Static guard for motion-induced visibility loss.

Ported from md-to-html-report-v3.0.1-motion-visibility-safety
scripts/validate_motion_visibility_safety.py onto the stdlib mini DOM.

This validator intentionally does NOT score design quality. It verifies one
property: when the motion runtime never runs (JS disabled / failed), semantic
content remains visible. It does NOT prescribe how that safety is achieved —
any statically provable fallback idiom passes (V1 no-js paired rules,
V2 conditional-hidden, V3 reduced-motion, V4 small carriers). Run on the base
report (delivery safety) and on the editable (edit-mode override present).
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import htmldom
import artifact_namespace
from htmldom import Node

DU_ATTRIBUTE = artifact_namespace.DU_ATTRIBUTE

IGNORE_CLASSES = {
    'js', 'no-js', 'motion-ready', 'in', 'on', 'visible', 'active',
    'loaded', 'ready', 'he-editing', 'reduced-motion',
}
STRUCTURAL_TAGS = {'main', 'section'}
BLOCK_TAGS = {'div', 'article', 'section', 'figure', 'table', 'ul', 'ol', 'header', 'aside'}
JS_STATE_CLASSES = ('js', 'no-js', 'motion-ready')


def css_rules(css: str):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css, flags=re.S):
        yield m.group(1).strip(), m.group(2).strip()


def _hidden_decl(decl: str) -> bool:
    return bool(re.search(r'(?:^|;)\s*opacity\s*:\s*0(?:\D|$)', decl, re.I)) or \
        bool(re.search(r'(?:^|;)\s*visibility\s*:\s*hidden\b', decl, re.I))


def hidden_motion_classes(css: str) -> set:
    out = set()
    for sel, decl in css_rules(css):
        if not _hidden_decl(decl):
            continue
        if not re.search(r'\.(?:js|motion-ready|rv|reveal|b-in|fade|animate|motion)', sel, re.I):
            continue
        for cls in re.findall(r'\.([A-Za-z_][\w-]*)', sel):
            if cls not in IGNORE_CLASSES:
                out.add(cls)
    return out


def _element_class_matches(el: Node, cls: str) -> bool:
    raw = el.attrs.get('class') or ''
    tokens = raw.split() if isinstance(raw, str) else raw
    return cls in tokens


def element_is_large_semantic_container(el: Node) -> bool:
    if el.tag in STRUCTURAL_TAGS:
        return True
    text_len = len(re.sub(r'\s+', ' ', htmldom.get_text(el).strip()))
    du_count = sum(1 for d in htmldom.iter_elements(el) if DU_ATTRIBUTE in d.attrs)
    return text_len > 1800 or du_count >= 3


def _fallback_makes_visible(decl: str) -> bool:
    return bool(re.search(r'opacity\s*:\s*1\b', decl, re.I)) or \
        bool(re.search(r'visibility\s*:\s*visible\b', decl, re.I))


def _selector_targets_cls(sel: str, cls: str) -> bool:
    """True only when the selector matches the class WITHOUT extra state
    conditions (`.b-in` or `.b-in .child`), NOT `.b-in.on` / `.b-in:hover`.
    Compound selectors only apply after runtime state, so they cannot prove
    static no-JS visibility."""
    for part in sel.split(','):
        part = part.strip()
        m = re.search(rf'\.{re.escape(cls)}(?![\w-])', part)
        if not m:
            continue
        # token immediately after .cls (or end) must not be another state class
        rest = part[m.end():]
        nxt = re.match(r'\.([A-Za-z_][\w-]*)', rest)
        if nxt and nxt.group(1) not in ('on', 'in'):
            continue  # pseudo/compound we don't understand -> treat as not covering
        if nxt:
            # `.cls.on` / `.cls.in` — runtime-state only, never a static proof
            continue
        return True
    return False


def classify_fallback_idioms(css: str, html_root: Node, js: str, hidden_classes: set) -> dict:
    """Property check — which fallback idioms are statically provable.

    A hidden class is SAFE if at least one idiom below covers EVERY rule that
    hides it. Otherwise the class can hide content with no JS-failure proof.
    """
    rules = list(css_rules(css))

    covered = {cls: [] for cls in hidden_classes}
    uncovered_rules = []

    for sel, decl in rules:
        for cls in hidden_classes:
            if not _hidden_decl(decl):
                continue
            if not _selector_targets_cls(sel, cls):
                continue
            safe = False
            # V1: paired no-js / reduced-motion fallback — html.no-js .b-in{opacity:1}
            if any(state in sel for state in ('no-js', 'reduced-motion')) and _fallback_makes_visible(decl):
                safe = True
            # V1b: the HIDING rule itself is conditional on JS state classes
            elif any(st in sel for st in JS_STATE_CLASSES) and any(st in sel for st in ('motion-ready', 'js')):
                safe = True
            # V2: an unconditional visible rule for the same class (.rv{opacity:1!important})
            if not safe:
                for sel2, decl2 in rules:
                    if _selector_targets_cls(sel2, cls) and _fallback_makes_visible(decl2) \
                            and not any(st in sel2 for st in JS_STATE_CLASSES):
                        safe = True
                        break
            if safe:
                covered[cls].append(sel.strip())
            else:
                uncovered_rules.append({'class': cls, 'selector': sel.strip()})

    idioms = {}
    if any(covered[cls] for cls in covered):
        idioms['V1_nojs_or_conditional'] = True
    reduced = re.search(r'@media[^{]*prefers-reduced-motion[^{]*\{.*', css, re.I | re.S)
    if reduced and any(_fallback_makes_visible(chunk) for chunk in re.findall(r'\{([^{}]*)\}', reduced.group(0))):
        idioms['V3_reduced_motion'] = True
    return {'idioms': idioms, 'covered': covered, 'uncovered': uncovered_rules}


def motion_density(css: str, html_root: Node, js: str) -> dict:
    """Observation-only metric. Never contributes to pass/fail — it exists so
    repair loops can diff expressiveness before/after a fix (R3 of the repair
    charter): deletions that flatten motion are visible instead of silent."""
    density = {
        'transition_rules': len(re.findall(r'transition\s*:', css, re.I)),
        'transition_properties': len(re.findall(r'transition\s*:[^;]+', css, re.I)),
        'keyframes_blocks': len(re.findall(r'@keyframes\b', css, re.I)),
        'animation_declarations': len(re.findall(r'animation\s*:', css, re.I)),
        'reveal_elements': sum(
            1 for el in htmldom.iter_elements(html_root)
            if any(_element_class_matches(el, cls) for cls in ('rv', 'reveal', 'b-in', 'fade', 'animate', 'motion'))
        ),
        'io_observers': len(re.findall(r'IntersectionObserver', js)),
        'transform_declarations': len(re.findall(r'transform\s*:', css, re.I)),
    }
    density['total'] = sum(density.values())
    return density


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', required=True, type=Path)
    ap.add_argument('--editable', action='store_true')
    args = ap.parse_args()

    text = args.html.read_text(encoding='utf-8')
    root, _ = htmldom.parse_html(text)
    styles = [s for s in htmldom.iter_elements(root) if s.tag == 'style']
    scripts = [
        s for s in htmldom.iter_elements(root)
        if s.tag == 'script' and (s.attrs.get('type') or '').lower() != 'application/json'
    ]
    css = '\n'.join(htmldom.get_text(s) for s in styles)
    js = '\n'.join(htmldom.get_text(s) for s in scripts)

    failures = []
    warnings = []
    evidence = {}

    hidden_classes = hidden_motion_classes(css)
    evidence['hidden_motion_classes'] = sorted(hidden_classes)

    fallback = classify_fallback_idioms(css, root, js, hidden_classes) if hidden_classes \
        else {'idioms': {}, 'covered': {}, 'uncovered': []}
    evidence['fallback_idioms'] = fallback['idioms']
    evidence['uncovered_hidden_rules'] = fallback['uncovered'][:20]

    # The core property: every hidden motion class must be covered by at
    # least one statically provable fallback idiom.
    if fallback['uncovered']:
        failures.append('HIDDEN_CONTENT_WITHOUT_JS_FAILURE_FALLBACK')
        if len(fallback['idioms']) == 0:
            failures.append('MOTION_RUNTIME_FAILURE_CAN_HIDE_CONTENT')
    elif hidden_classes and not fallback['idioms']:
        failures.append('MOTION_RUNTIME_FAILURE_CAN_HIDE_CONTENT')

    risky = []
    for cls in sorted(hidden_classes):
        for el in htmldom.iter_elements(root):
            if _element_class_matches(el, cls) and element_is_large_semantic_container(el):
                risky.append({
                    'tag': el.tag,
                    'id': el.attrs.get('id'),
                    'class': cls,
                    'text_chars': len(htmldom.get_text(el).strip()),
                    'descendant_du': sum(1 for d in htmldom.iter_elements(el) if DU_ATTRIBUTE in d.attrs),
                })
    # V4: small-carrier exemption — hidden reveal on small units is low risk
    # when a fallback idiom exists; large structural carriers are held to the
    # strict property regardless.
    evidence['large_hidden_motion_carriers'] = risky[:50]
    if risky:
        failures.append('LARGE_STRUCTURAL_HIDDEN_REVEAL')

    thresholds = []
    for x in re.findall(r'threshold\s*:\s*([0-9]*\.?[0-9]+)', js, flags=re.I):
        try:
            thresholds.append(float(x))
        except ValueError:
            pass
    evidence['intersection_thresholds'] = thresholds
    if risky and any(t >= 0.10 for t in thresholds):
        failures.append('HIGH_THRESHOLD_WITH_LARGE_HIDDEN_CARRIER')

    motion_ids = sum(1 for e in htmldom.iter_elements(root) if 'data-motion-reveal' in e.attrs)
    evidence['data_motion_reveal_count'] = motion_ids
    if hidden_classes and motion_ids == 0:
        warnings.append('NO_DATA_MOTION_REVEAL_IDENTITY')

    # R3 of the repair charter: expressiveness observation. Pure metric, no
    # pass/fail influence — written into evidence so before/after a repair the
    # diff is machine-readable in run-state via editor-validation-result.json.
    evidence['motion_density'] = motion_density(css, root, js)

    if args.editable:
        has_editor_override = bool(re.search(
            r'he-editing[^{}]*(?:rv|reveal|b-in|data-motion-reveal).*?\{[^{}]*(?:opacity\s*:\s*1|visibility\s*:\s*visible)',
            css, re.I | re.S))
        if not has_editor_override:
            failures.append('EDIT_MODE_MOTION_VISIBILITY_OVERRIDE_MISSING')

    result = {
        'status': 'PASS' if not failures else 'FAIL',
        'file': str(args.html),
        'failures': failures,
        'warnings': warnings,
        'evidence': evidence,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
