#!/usr/bin/env python3
"""Static guard for motion-induced visibility loss.

Ported from md-to-html-report-v3.0.1-motion-visibility-safety
scripts/validate_motion_visibility_safety.py onto the stdlib mini DOM.

This validator intentionally does NOT score design quality. It detects
high-risk patterns where semantic content can remain invisible because a
motion runtime never reaches its reveal condition. Run on the base report
(delivery safety) and on the editable (edit-mode override present).
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


def css_rules(css: str):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css, flags=re.S):
        yield m.group(1).strip(), m.group(2).strip()


def hidden_motion_classes(css: str) -> set:
    out = set()
    for sel, decl in css_rules(css):
        hidden = bool(re.search(r'(?:^|;)\s*opacity\s*:\s*0(?:\D|$)', decl, re.I)) or \
                 bool(re.search(r'(?:^|;)\s*visibility\s*:\s*hidden\b', decl, re.I))
        if not hidden:
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

    unconditional_hidden = []
    for sel, decl in css_rules(css):
        hidden = bool(re.search(r'(?:^|;)\s*opacity\s*:\s*0(?:\D|$)', decl, re.I)) or \
                 bool(re.search(r'visibility\s*:\s*hidden', decl, re.I))
        if not hidden:
            continue
        for cls in hidden_classes:
            if re.search(rf'(^|[\s,>+~])\.{re.escape(cls)}(?:[:.#\s,>+~{{]|$)', sel) \
                    and not re.search(r'\.(?:js|motion-ready|no-js)', sel):
                unconditional_hidden.append({'class': cls, 'selector': sel.strip()})
    evidence['unconditional_hidden_motion_rules'] = unconditional_hidden

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

    root_gate = bool(re.search(r"documentElement\.classList\.add\s*\(\s*['\"]js['\"]", js))
    remove_nojs = bool(re.search(r"documentElement\.classList\.remove\s*\(\s*['\"]no-js['\"]", js))
    has_motion_ready = 'motion-ready' in text
    evidence['immediate_js_gate'] = root_gate
    evidence['remove_no_js_gate'] = remove_nojs
    evidence['motion_ready_gate_present'] = has_motion_ready
    if hidden_classes and not has_motion_ready and (root_gate or remove_nojs or unconditional_hidden):
        failures.append('MOTION_RUNTIME_FAILURE_CAN_HIDE_CONTENT')

    if hidden_classes and 'prefers-reduced-motion' not in css:
        failures.append('NO_REDUCED_MOTION_FALLBACK')
    elif hidden_classes:
        reduced_blocks = re.findall(
            r'@media\s*\(prefers-reduced-motion\s*:\s*reduce\)\s*\{(.*?)\}\s*', css, flags=re.I | re.S)
        joined = '\n'.join(reduced_blocks)
        if not re.search(r'opacity\s*:\s*1|visibility\s*:\s*visible', joined, re.I):
            warnings.append('REDUCED_MOTION_FALLBACK_NOT_EXPLICITLY_VISIBLE')

    if args.editable:
        has_editor_override = bool(re.search(
            r'he-editing[^{}]*(?:rv|reveal|b-in|data-motion-reveal).*?\{[^{}]*(?:opacity\s*:\s*1|visibility\s*:\s*visible)',
            css, re.I | re.S))
        if not has_editor_override:
            failures.append('EDIT_MODE_MOTION_VISIBILITY_OVERRIDE_MISSING')

    motion_ids = sum(1 for e in htmldom.iter_elements(root) if 'data-motion-reveal' in e.attrs)
    evidence['data_motion_reveal_count'] = motion_ids
    if hidden_classes and motion_ids == 0:
        warnings.append('NO_DATA_MOTION_REVEAL_IDENTITY')

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
