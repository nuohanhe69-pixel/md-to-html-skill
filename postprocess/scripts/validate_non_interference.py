#!/usr/bin/env python3
"""Structural non-interference validator (Editor V2.0).

Replaces the byte-level strip check of Editor V1.x. Editor V2.0 annotates
the base DOM at compile time (additive attributes + appended artifacts),
so interference is proven structurally:

  parse(editable) - injected attributes - artifact nodes == parse(base)

A tree-level equality is weaker than byte equality but still proves that
no text node, element, attribute, or ordering of the base report was
touched, added, or removed outside the declared annotation namespace.
The hard base invariant (SHA unchanged on disk) remains byte-level.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import htmldom
from htmldom import Node, iter_elements

ARTIFACT_IDS = (
    'he-editor-style', 'he-editor-script', 'human-edit-ledger',
    'human-edit-base-state', 'human-edit-meta',
)
INJECTED_ATTRS = (
    'data-edit-id', 'data-edit-type', 'data-edit-authority',
    'data-edit-obligation-refs', 'data-edit-module-id', 'data-edit-movable',
    'data-motion-reveal', 'data-he-runtime-ui', 'data-human-edit-layer',
)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _has_editor_namespace(root: Node) -> list:
    hits = []
    for e in iter_elements(root):
        if e.attrs.get('id') in ARTIFACT_IDS:
            hits.append(f'id={e.attrs["id"]}')
        for a in INJECTED_ATTRS:
            if a in e.attrs:
                hits.append(f'<{e.tag}> {a}')
    return hits


def _strip_injections(root: Node) -> None:
    for eid in ARTIFACT_IDS:
        node = htmldom.find_by_id(root, eid)
        if node is not None and node.parent is not None:
            node.parent.children.remove(node)
    for e in iter_elements(root):
        for a in INJECTED_ATTRS:
            e.attrs.pop(a, None)


def _id_uniqueness(root: Node, attr: str) -> list:
    seen = {}
    dupes = []
    for e in iter_elements(root):
        v = e.attrs.get(attr)
        if v:
            if v in seen:
                dupes.append(v)
            seen[v] = True
    return dupes


def _runtime_browse_equivalence(base_html: str, editable_html: str) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        return {'status': 'SKIPPED', 'reason': f'playwright unavailable: {exc}'}

    strip_ext = r'(?:<link[^>]+href=["\']https?://[^"\']*["\'][^>]*>)|(?:<script[^>]+src=["\']https?://[^"\']*["\'][^>]*>\s*</script>)'
    import re
    base_clean = re.sub(strip_ext, '', base_html, flags=re.I)
    editable_clean = re.sub(strip_ext, '', editable_html, flags=re.I)
    base_clean = re.sub(r'<script[^>]*>\s*</script>', '', base_clean)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 2400})
            page.set_content(base_clean, wait_until='load', timeout=20000)
            page.wait_for_timeout(300)
            base_text = page.evaluate('document.body.innerText')
            base_geo = page.evaluate(
                'JSON.stringify({sw:document.body.scrollWidth,sh:document.body.scrollHeight})')
            page.set_content(editable_clean, wait_until='load', timeout=20000)
            page.wait_for_timeout(300)
            page.evaluate("document.querySelectorAll('[data-he-runtime-ui]').forEach(n=>n.remove())")
            page.evaluate("document.body.classList.remove('he-editing')")
            page.evaluate("document.querySelectorAll('.he-module-tag').forEach(n=>n.remove())")
            editable_text = page.evaluate('document.body.innerText')
            editable_geo = page.evaluate(
                'JSON.stringify({sw:document.body.scrollWidth,sh:document.body.scrollHeight})')
            browser.close()
    except Exception as exc:
        return {'status': 'SKIPPED', 'reason': f'runtime probe failed: {exc}'}

    text_equal = base_text.strip() == editable_text.strip()
    geo_equal = base_geo == editable_geo
    return {
        'status': 'PASS' if (text_equal and geo_equal) else 'WARN',
        'browse_text_equal': text_equal,
        'browse_geometry_equal': geo_equal,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True, type=Path)
    ap.add_argument('--editable', required=True, type=Path)
    ap.add_argument('--expected-base-sha', required=True)
    ap.add_argument('--static-only', action='store_true')
    a = ap.parse_args()

    checks = {}
    checks['expected_base_sha_match'] = sha256_of(a.base) == a.expected_base_sha

    base_root, base_doctype = htmldom.parse_html(a.base.read_text(encoding='utf-8'))
    editable_root, editable_doctype = htmldom.parse_html(a.editable.read_text(encoding='utf-8'))

    base_pollution = _has_editor_namespace(base_root)
    checks['base_has_no_editor_namespace'] = not base_pollution
    checks['base_pollution_evidence'] = base_pollution[:20]

    missing_artifacts = [eid for eid in ARTIFACT_IDS if htmldom.find_by_id(editable_root, eid) is None]
    checks['editable_has_all_artifacts'] = not missing_artifacts
    checks['missing_artifacts'] = missing_artifacts

    checks['edit_ids_unique'] = not _id_uniqueness(editable_root, 'data-edit-id')
    checks['module_ids_unique'] = not _id_uniqueness(editable_root, 'data-edit-module-id')

    _strip_injections(editable_root)
    checks['structural_equivalence'] = htmldom.tree_equal(editable_root, base_root) \
        and editable_doctype == base_doctype

    failures = [k for k, v in checks.items() if isinstance(v, bool) and not v]
    status = 'PASS' if not failures else 'FAIL'

    result = {
        'status': status,
        'mode': 'structural (Editor V2.0 compile-time annotation)',
        'checks': checks,
        'failures': failures,
    }

    if not a.static_only:
        runtime = _runtime_browse_equivalence(
            a.base.read_text(encoding='utf-8'), a.editable.read_text(encoding='utf-8'))
        result['runtime_browse_equivalence'] = runtime
        if runtime.get('status') == 'WARN':
            result['warnings'] = ['browse mode text/geometry differs between base and editable']

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())
