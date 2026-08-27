#!/usr/bin/env python3
"""Compile-time structural annotation injector (Editor V2.0).

Lineage: ported from md-to-html-report-v3.0.1-motion-visibility-safety
scripts/inject_editor.py, rewritten on the stdlib mini DOM (htmldom) so the
deterministic postprocess subsystem keeps zero third-party dependencies.

Contract (see postprocess/references/editor-contract.md):
- Injects NOTHING at runtime discovery time. The whole DOM is parsed and
  annotated BEFORE the editable file is written.
- Annotations are strictly additive: new attributes on existing elements +
  artifact nodes appended to the end of <head>/<body>. No base node is
  reordered, rewritten, or removed.
- Non-interference is proven structurally (validate_non_interference.py):
  stripping the injected attributes and artifact nodes must yield a DOM tree
  identical to the base tree.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import htmldom
from htmldom import Node, iter_elements, make_element

EDITABLE_TAGS = {
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'th', 'td',
    'blockquote', 'figcaption', 'dt', 'dd', 'label', 'button', 'small',
}
BLOCK_CHILDREN = {
    'div', 'section', 'article', 'table', 'ul', 'ol', 'figure',
    'header', 'footer', 'nav', 'aside',
}
MOTION_STATE_CLASSES = {
    'js', 'no-js', 'motion-ready', 'in', 'on', 'visible',
    'active', 'loaded', 'ready', 'he-editing',
}
ARTIFACT_IDS = (
    'he-editor-style', 'he-editor-script', 'human-edit-ledger',
    'human-edit-base-state', 'human-edit-meta',
)
INJECTED_ATTRS = (
    'data-edit-id', 'data-edit-type', 'data-edit-authority',
    'data-edit-obligation-refs', 'data-edit-module-id', 'data-edit-movable',
    'data-motion-reveal',
)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_norm(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def css_rules(css: str):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css, flags=re.S):
        yield m.group(1).strip(), m.group(2).strip()


def detect_motion_reveal_classes(css: str) -> set:
    out = set()
    for sel, decl in css_rules(css):
        hidden = bool(re.search(r'(?:^|;)\s*opacity\s*:\s*0(?:\D|$)', decl, re.I)) or \
                 bool(re.search(r'(?:^|;)\s*visibility\s*:\s*hidden\b', decl, re.I))
        if not hidden:
            continue
        if not re.search(r'\.(?:js|motion-ready|rv|reveal|b-in|fade|animate|motion)', sel, re.I):
            continue
        for cls in re.findall(r'\.([A-Za-z_][\w-]*)', sel):
            if cls not in MOTION_STATE_CLASSES:
                out.add(cls)
    return out


def nearest_du(node: Node) -> str:
    cur = node
    while cur is not None and cur.kind == 'element':
        du = cur.attrs.get('data-du')
        if du:
            return text_norm(du).split()[0]
        cur = cur.parent
    return 'PAGE'


def _inside_runtime_ui(node: Node) -> bool:
    cur = node.parent
    while cur is not None and cur.kind == 'element':
        if 'data-he-runtime-ui' in cur.attrs:
            return True
        cur = cur.parent
    return False


def is_leaf_editable(el: Node) -> bool:
    if el.tag not in EDITABLE_TAGS and el.tag != 'span':
        return False
    txt = text_norm(htmldom.get_text(el))
    if not txt:
        return False
    if _inside_runtime_ui(el):
        return False
    if el.tag == 'span':
        if any(c.kind == 'element' for c in el.children):
            return False
        if len(txt) > 180:
            return False
        return True
    for c in el.children:
        if c.kind == 'element' and c.tag in BLOCK_CHILDREN:
            return False
    return True


def load_authority_map(path: Path | None):
    if not path or not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def apply_authority_map(root: Node, amap: dict):
    if not amap:
        return
    for rule in amap.get('targets', []):
        authority = rule.get('authority', 'human-editable')
        refs = [str(r) for r in rule.get('obligation_refs', [])]
        if rule.get('selector'):
            targets = htmldom.select(root, rule['selector'])
        else:
            du = rule.get('du')
            needle = text_norm(rule.get('contains_text', ''))
            targets = [
                e for e in iter_elements(root)
                if 'data-edit-id' in e.attrs
                and (du is None or nearest_du(e) == du)
                and (not needle or needle in text_norm(htmldom.get_text(e)))
            ]
        for t in targets:
            t.attrs['data-edit-authority'] = authority
            if refs:
                t.attrs['data-edit-obligation-refs'] = ' '.join(refs)
    for rule in amap.get('modules', []):
        if rule.get('selector'):
            mods = htmldom.select(root, rule['selector'])
        else:
            du = rule.get('du')
            mods = [
                e for e in iter_elements(root)
                if 'data-edit-module-id' in e.attrs and (du is None or nearest_du(e) == du)
            ]
        for m in mods:
            if 'data-edit-module-id' in m.attrs:
                m.attrs['data-edit-movable'] = 'true' if rule.get('movable') else 'false'


def build_base_state(root: Node) -> dict:
    elements = {}
    modules = {}
    for e in iter_elements(root):
        eid = e.attrs.get('data-edit-id')
        if eid:
            elements[eid] = {
                'text': htmldom.get_text(e),
                'style': e.attrs.get('style') or '',
                'authority': e.attrs.get('data-edit-authority', 'human-editable'),
            }
        mid = e.attrs.get('data-edit-module-id')
        if mid:
            parent = e.parent
            idx = sum(
                1 for c in parent.children
                if c.kind == 'element' and 'data-edit-module-id' in c.attrs
            ) - 1
            modules[mid] = {
                'style': e.attrs.get('style') or '',
                'index': max(idx, 0),
                'movable': e.attrs.get('data-edit-movable', 'false') == 'true',
                'du': nearest_du(e),
            }
    return {'schema_version': '1.0', 'elements': elements, 'modules': modules}


def _json_script_node(script_id: str, payload: dict) -> Node:
    content = json.dumps(payload, ensure_ascii=False, indent=2).replace('</script>', '<\\/script>')
    return make_element('script', {'id': script_id, 'type': 'application/json'}, content)


def inject(input_html: Path, output_html: Path, editor_dir: Path,
           authority_map: Path | None, artifact_version: str) -> dict:
    before = sha256_of(input_html)
    base_text = input_html.read_text(encoding='utf-8')
    root, doctype = htmldom.parse_html(base_text)

    head = htmldom.first_tag(root, 'head')
    body = htmldom.first_tag(root, 'body')
    if head is None or body is None:
        raise ValueError('input html must contain <head> and <body>')

    for e in iter_elements(root):
        if e.attrs.get('id') in ARTIFACT_IDS:
            raise ValueError('input already contains Human Edit Layer markers (refuse to re-inject)')
        if 'data-edit-id' in e.attrs or 'data-edit-module-id' in e.attrs:
            raise ValueError('input already contains edit annotations (refuse to re-inject)')

    css_text = '\n'.join(htmldom.get_text(s) for s in iter_elements(root) if s.tag == 'style')
    motion_classes = detect_motion_reveal_classes(css_text)
    motion_reveal_count = 0
    for cls in sorted(motion_classes):
        for e in iter_elements(root):
            if htmldom.has_class(e, cls) and 'data-motion-reveal' not in e.attrs:
                e.attrs['data-motion-reveal'] = 'true'

    module_counts = {}
    for m in iter_elements(root):
        if 'data-du' not in m.attrs:
            continue
        du = nearest_du(m)
        module_counts[du] = module_counts.get(du, 0) + 1
        m.attrs['data-edit-module-id'] = f'{du}.module.{module_counts[du]:03d}'
        m.attrs['data-edit-movable'] = 'false'

    elem_counts = {}
    for e in iter_elements(root):
        if not is_leaf_editable(e):
            continue
        du = nearest_du(e)
        key = (du, e.tag)
        elem_counts[key] = elem_counts.get(key, 0) + 1
        e.attrs['data-edit-id'] = f'{du}.{e.tag}.{elem_counts[key]:03d}'
        e.attrs['data-edit-type'] = 'text'
        e.attrs['data-edit-authority'] = 'human-editable'

    apply_authority_map(root, load_authority_map(authority_map))

    motion_reveal_count = sum(1 for e in iter_elements(root) if 'data-motion-reveal' in e.attrs)
    editable_elements = sum(1 for e in iter_elements(root) if 'data-edit-id' in e.attrs)
    editable_modules = sum(1 for e in iter_elements(root) if 'data-edit-module-id' in e.attrs)
    locked_targets = sum(
        1 for e in iter_elements(root)
        if e.attrs.get('data-edit-authority', 'human-editable') != 'human-editable'
    )

    base_state = build_base_state(root)

    css_path = editor_dir / 'editor.css'
    js_path = editor_dir / 'editor.js'
    if not css_path.exists() or not js_path.exists():
        raise ValueError(f'editor runtime assets missing under {editor_dir}')

    style_node = make_element(
        'style', {'id': 'he-editor-style', 'data-human-edit-layer': 'runtime'},
        css_path.read_text(encoding='utf-8'),
    )
    style_node.parent = head
    head.children.append(style_node)

    meta = {
        'schema_version': '1.0',
        'artifact_version': artifact_version,
        'base_artifact': input_html.name,
        'base_report_sha256': before,
        'mode': 'human-only',
        'source_backflow': False,
        'editable_elements': editable_elements,
        'editable_modules': editable_modules,
        'locked_targets': locked_targets,
        'motion_reveal_elements': motion_reveal_count,
        'motion_visibility_safety': 'EDIT_MODE_FORCE_VISIBLE',
    }
    ledger = {
        'schema_version': '1.0',
        'artifact_version': artifact_version,
        'base_report_sha256': before,
        'history': [],
        'cursor': -1,
        'effective_patches': [],
        'source_backflow': 'FORBIDDEN',
        'ai_editing': 'DISABLED',
    }

    for node in (
        _json_script_node('human-edit-base-state', base_state),
        _json_script_node('human-edit-ledger', ledger),
        _json_script_node('human-edit-meta', meta),
        make_element('script', {'id': 'he-editor-script', 'data-human-edit-layer': 'runtime'},
                     js_path.read_text(encoding='utf-8')),
    ):
        node.parent = body
        body.children.append(node)

    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(htmldom.serialize_html(root, doctype), encoding='utf-8')

    after = sha256_of(input_html)
    if before != after:
        raise ValueError('base report changed during injection — abort')

    return {
        'base_report': str(input_html),
        'editable_report': str(output_html),
        'base_report_sha256': before,
        'base_unchanged': True,
        'schema_version': '1.0',
        'mode': 'human-only',
        'base_artifact': input_html.name,
        'artifact_version': artifact_version,
        'editable_elements': editable_elements,
        'editable_modules': editable_modules,
        'locked_targets': locked_targets,
        'motion_reveal_elements': motion_reveal_count,
        'motion_visibility_safety': 'EDIT_MODE_FORCE_VISIBLE',
        'authority_map_applied': bool(authority_map and authority_map.exists()),
        'source_backflow': False,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description='compile-time editor annotation injector')
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--editor-dir', required=True, type=Path)
    ap.add_argument('--authority-map', type=Path, default=None)
    ap.add_argument('--artifact-version', default='v001')
    a = ap.parse_args()
    try:
        result = inject(a.input, a.output, a.editor_dir, a.authority_map, a.artifact_version)
    except Exception as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, ensure_ascii=False, indent=2))
        return 2
    result['status'] = 'PASS'
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
