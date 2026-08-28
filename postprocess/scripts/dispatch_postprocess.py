#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}

def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def update_run_state(root: Path, result: dict):
    rs = root / 'workspace' / 'run-state.json'
    if not rs.exists():
        return
    data = load_json(rs)
    data['postprocess_extension_version'] = 'Editor Postprocess V2.0 (compile-time annotation)'
    data['postprocess_status'] = result.get('status', 'FAIL')
    data['editable_output_path'] = 'editable/report-editable.html'
    data['editor_validation_result_path'] = 'editable/editor-validation-result.json'
    save_json(rs, data)

def append_analysis(root: Path, result: dict):
    p = root / 'analysis.md'
    if not p.exists():
        return
    txt = p.read_text(encoding='utf-8')
    marker = '## Post-Generation Editor Extension V2.0'
    if marker in txt:
        return
    status = result.get('status', 'FAIL')
    section = (
        f"\n\n{marker}\n\n"
        "```yaml\n"
        "postprocess_extension: Editor Postprocess V2.0 (compile-time annotation)\n"
        f"postprocess_status: {status}\n"
        "editable_output: editable/report-editable.html\n"
        "validation_result: editable/editor-validation-result.json\n"
        "```\n"
    )
    p.write_text(txt + section, encoding='utf-8')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output-root', required=True)
    p.add_argument('--runtime-qa', choices=['auto', 'off', 'required'], default='auto')
    a = p.parse_args()

    base = Path(a.input).resolve()
    root = Path(a.output_root).resolve()
    here = Path(__file__).resolve().parent
    editable = root / 'editable' / 'report-editable.html'
    result_json = root / 'editable' / 'editor-validation-result.json'
    status_json = root / 'editable' / 'postprocess-status.json'
    cmd = [
        sys.executable, str(here/'run_postprocess.py'),
        '--input', str(base),
        '--output', str(editable),
        '--result-json', str(result_json),
        '--runtime-qa', a.runtime_qa,
    ]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        result = load_json(result_json)
        if not result:
            result = {'status': 'FAIL', 'error': 'run_postprocess returned no result json', 'stdout': r.stdout, 'stderr': r.stderr}
        result['base_report_path'] = str(base)
        save_json(status_json, result)
        update_run_state(root, result)
        append_analysis(root, result)
        ok = result.get('status') in ('PASS', 'PASS_WITH_RUNTIME_WARNING') and editable.exists()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if ok else 2
    except subprocess.TimeoutExpired:
        result = {
            'status': 'FAIL',
            'error': 'dispatcher timeout after 90s',
            'base_report_path': str(base),
            'editable_report_path': str(editable),
        }
        save_json(result_json, result)
        save_json(status_json, result)
        update_run_state(root, result)
        append_analysis(root, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
