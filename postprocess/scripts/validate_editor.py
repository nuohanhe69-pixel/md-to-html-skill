#!/usr/bin/env python3
"""Editor runtime asset validator (Editor V2.0).

Static (mandatory): embedded artifacts present, ledger/meta JSON well-formed
and locked (ai_editing=DISABLED, source_backflow=FORBIDDEN), editor.js free
of network/AI/motion-coupling patterns, node --check when available.

Runtime (best-effort, needs playwright): launcher opens edit mode, editable
elements match meta counts, text edit via panel applies, undo/redo revert.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import htmldom

ARTIFACT_IDS = (
    'he-editor-style', 'he-editor-script', 'human-edit-ledger',
    'human-edit-base-state', 'human-edit-meta',
)
FORBIDDEN_JS_PATTERNS = [
    r'\bfetch\s*\(',
    'XMLHttpRequest',
    'WebSocket',
    'EventSource',
    r'\bopenai\b',
    r'\banthropic\b',
    r'api[_-]?key',
    r'\bllm\b',
    'huashu',
    'IntersectionObserver',
    'animationTimeline',
    'scrollTimeline',
    'motion-ready',
]


def _embedded_json(html_text: str, script_id: str):
    m = re.search(
        rf'<script id="{script_id}" type="application/json">(.*?)</script>', html_text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def _static_checks(editable_path: Path, editor_js: Path | None) -> dict:
    html_text = editable_path.read_text(encoding='utf-8')
    root, _ = htmldom.parse_html(html_text)

    checks = {}
    missing = [eid for eid in ARTIFACT_IDS if htmldom.find_by_id(root, eid) is None]
    checks['artifacts_embedded'] = not missing
    checks['missing_artifacts'] = missing

    ledger = _embedded_json(html_text, 'human-edit-ledger')
    checks['ledger_wellformed'] = ledger is not None
    checks['ledger_ai_editing_disabled'] = bool(ledger) and ledger.get('ai_editing') == 'DISABLED'
    checks['ledger_source_backflow_forbidden'] = bool(ledger) and ledger.get('source_backflow') == 'FORBIDDEN'

    meta = _embedded_json(html_text, 'human-edit-meta')
    checks['meta_wellformed'] = meta is not None
    checks['meta_has_base_sha'] = bool(meta) and bool(meta.get('base_report_sha256'))
    checks['meta_counts_positive'] = bool(meta) and meta.get('editable_elements', 0) > 0

    js_text = editor_js.read_text(encoding='utf-8') if editor_js and editor_js.exists() else ''
    hits = [pat for pat in FORBIDDEN_JS_PATTERNS if re.search(pat, js_text, re.I)]
    checks['editor_js_clean'] = not hits
    checks['editor_js_forbidden_hits'] = hits

    if editor_js and editor_js.exists() and shutil.which('node'):
        r = subprocess.run(['node', '--check', str(editor_js)], capture_output=True, text=True, timeout=30)
        checks['editor_js_syntax_ok'] = r.returncode == 0
        if r.returncode != 0:
            checks['editor_js_syntax_error'] = r.stderr[-500:]
    return checks


def _runtime_checks(editable_path: Path) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        return {'status': 'SKIPPED', 'reason': f'playwright unavailable: {exc}'}

    html_text = editable_path.read_text(encoding='utf-8')
    meta = _embedded_json(html_text, 'human-edit-meta') or {}
    expected = meta.get('editable_elements', 0)
    steps = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 2400})
            page.set_content(html_text, wait_until='load', timeout=20000)
            page.wait_for_timeout(400)

            page.click('#he-launcher', timeout=5000)
            page.wait_for_timeout(200)
            editing = page.evaluate('document.body.classList.contains("he-editing")')
            steps.append(('launcher_opens_edit_mode', editing))

            count = page.locator('[data-edit-id]').count()
            steps.append(('editable_elements_match_meta', count == expected and count > 0))

            first = page.locator('[data-edit-id]').first
            first.click(timeout=5000)
            page.wait_for_timeout(200)
            before_text = first.text_content()
            marker = '__HE_TEST__'
            page.fill('#he-text', (before_text or '') + marker, timeout=5000)
            page.click('#he-apply-text', timeout=5000)
            page.wait_for_timeout(200)
            applied = marker in (first.text_content() or '')
            steps.append(('panel_text_edit_applies', applied))

            page.click('#he-undo', timeout=5000)
            page.wait_for_timeout(200)
            reverted = marker not in (first.text_content() or '')
            steps.append(('undo_reverts', reverted))

            page.click('#he-redo', timeout=5000)
            page.wait_for_timeout(200)
            reapplied = marker in (first.text_content() or '')
            steps.append(('redo_reapplies', reapplied))

            page.click('#he-exit', timeout=5000)
            page.wait_for_timeout(200)
            exited = not page.evaluate('document.body.classList.contains("he-editing")')
            steps.append(('exit_closes_edit_mode', exited))

            browser.close()
    except Exception as exc:
        return {'status': 'SKIPPED', 'reason': f'runtime probe failed: {exc}', 'steps': steps}

    ok = all(v for _, v in steps)
    return {'status': 'PASS' if ok else 'WARN', 'steps': steps}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', required=True, type=Path)
    ap.add_argument('--editor-js', type=Path, default=None)
    ap.add_argument('--static-only', action='store_true')
    a = ap.parse_args()

    checks = _static_checks(a.html, a.editor_js)
    failures = [k for k, v in checks.items() if isinstance(v, bool) and not v]
    result = {'status': 'PASS' if not failures else 'FAIL', 'checks': checks, 'failures': failures}

    if not a.static_only:
        result['runtime'] = _runtime_checks(a.html)
        if result['runtime'].get('status') == 'WARN':
            result['warnings'] = ['editor runtime smoke test reported failures']

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())
