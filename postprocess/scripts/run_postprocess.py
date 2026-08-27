#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(cmd, timeout=45):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed ({r.returncode}): {' '.join(cmd)}\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}")
    return r.stdout.strip()

def try_runtime(cmd, timeout=25):
    try:
        out = run(cmd, timeout=timeout)
        data = json.loads(out)
        return {'status': data.get('status', 'UNKNOWN'), 'result': data}
    except subprocess.TimeoutExpired:
        return {'status': 'SKIPPED_TIMEOUT', 'reason': f'runtime QA exceeded {timeout}s'}
    except Exception as e:
        return {'status': 'WARNING', 'reason': str(e)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--result-json')
    p.add_argument('--runtime-qa', choices=['auto', 'off', 'required'], default='auto')
    a = p.parse_args()
    base = Path(a.input).resolve()
    out = Path(a.output).resolve()
    here = Path(__file__).resolve().parent
    editor_dir = here.parent / 'editor'
    before = sha(base)
    result_path = Path(a.result_json).resolve() if a.result_json else None
    try:
        # Optional authority map: <output-root>/workspace/editable-authority-map.json
        authority_map = out.resolve().parent.parent / 'workspace' / 'editable-authority-map.json'
        inject_cmd = [sys.executable, str(here/'inject_editor.py'), '--input', str(base), '--output', str(out), '--editor-dir', str(editor_dir)]
        if authority_map.exists():
            inject_cmd += ['--authority-map', str(authority_map)]

        build = json.loads(run(inject_cmd))
        non = json.loads(run([sys.executable, str(here/'validate_non_interference.py'), '--base', str(base), '--editable', str(out), '--expected-base-sha', before, '--static-only']))
        editor = json.loads(run([sys.executable, str(here/'validate_editor.py'), '--html', str(out), '--editor-js', str(editor_dir/'editor.js'), '--static-only']))
        motion_base = json.loads(run([sys.executable, str(here/'validate_motion_visibility_safety.py'), '--html', str(base)]))
        motion_editable = json.loads(run([sys.executable, str(here/'validate_motion_visibility_safety.py'), '--html', str(out), '--editable']))
        required_pass = [non, editor, motion_base, motion_editable]
        if any(d.get('status') != 'PASS' for d in required_pass):
            failed = [d.get('file', k) for k, d in zip(['non_interference', 'editor', 'motion_base', 'motion_editable'], required_pass) if d.get('status') != 'PASS']
            raise RuntimeError(f'mandatory static validation failed: {failed}')

        runtime = {'mode': a.runtime_qa, 'non_interference': {'status': 'SKIPPED'}, 'editor': {'status': 'SKIPPED'}}
        runtime_warning = False
        if a.runtime_qa != 'off':
            runtime['non_interference'] = try_runtime([sys.executable, str(here/'validate_non_interference.py'), '--base', str(base), '--editable', str(out), '--expected-base-sha', before], timeout=30)
            runtime['editor'] = try_runtime([sys.executable, str(here/'validate_editor.py'), '--html', str(out), '--editor-js', str(editor_dir/'editor.js')], timeout=40)
            states = [runtime['non_interference']['status'], runtime['editor']['status']]
            runtime_warning = any(s not in ('PASS', 'SKIPPED') for s in states)
            if a.runtime_qa == 'required' and runtime_warning:
                raise RuntimeError(f'required runtime QA did not pass: {states}')

        after = sha(base)
        if before != after:
            raise RuntimeError('BASE_ARTIFACT_MUTATED')
        status = 'PASS_WITH_RUNTIME_WARNING' if runtime_warning else 'PASS'
        result = {
            'status': status,
            'base_report_path': str(base),
            'editable_report_path': str(out),
            'base_sha_before': before,
            'base_sha_after': after,
            'build': build,
            'non_interference': non,
            'editor_validation': editor,
            'motion_visibility': {'base': motion_base, 'editable': motion_editable},
            'runtime_qa': runtime,
        }
        payload = json.dumps(result, ensure_ascii=False, indent=2)
        if result_path:
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(payload, encoding='utf-8')
        print(payload)
        return 0
    except Exception as e:
        after = sha(base) if base.exists() else None
        fail = {
            'status': 'FAIL',
            'error': str(e),
            'base_report_path': str(base),
            'editable_report_path': str(out),
            'base_sha_before': before,
            'base_sha_after': after,
        }
        payload = json.dumps(fail, ensure_ascii=False, indent=2)
        if result_path:
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(payload, encoding='utf-8')
        print(payload)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
