#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PASS_STATES = {'PASS', 'PASS_WITH_RUNTIME_WARNING'}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def update_state(root: Path, **updates) -> None:
    rs = root / 'workspace' / 'run-state.json'
    if not rs.exists():
        return
    data = load_json(rs)
    data.update(updates)
    save_json(rs, data)


def validate_existing(root: Path, report: Path) -> tuple[bool, dict]:
    editable = root / 'editable' / 'report-editable.html'
    result_json = root / 'editable' / 'editor-validation-result.json'
    status_json = root / 'editable' / 'postprocess-status.json'
    result = load_json(status_json) or load_json(result_json)
    ok = (
        report.exists()
        and editable.exists()
        and result_json.exists()
        and status_json.exists()
        and result.get('status') in PASS_STATES
        and result.get('base_sha_before')
        and result.get('base_sha_after')
        and result.get('base_sha_before') == result.get('base_sha_after') == sha256(report)
    )
    return ok, result


def main() -> int:
    p = argparse.ArgumentParser(description='Required post-generation delivery finalizer')
    p.add_argument('--output-root', required=True)
    p.add_argument('--runtime-qa', choices=['auto', 'off', 'required'], default='auto')
    p.add_argument('--force', action='store_true', help='re-run dispatcher even if a valid editable artifact already exists')
    a = p.parse_args()

    root = Path(a.output_root).resolve()
    report = root / 'report.html'
    if not report.exists():
        update_state(
            root,
            postprocess_required=True,
            current_phase='POSTPROCESS',
            current_status='POSTPROCESS_BLOCKED',
            delivery_gate_status='BLOCKED',
            pending_tasks=['POSTPROCESS_FINALIZER', 'FINAL_DELIVERY'],
            last_artifact_failure='report.html missing before delivery finalizer',
        )
        print(json.dumps({'status': 'FAIL', 'error': 'report.html missing', 'report': str(report)}, ensure_ascii=False, indent=2))
        return 2

    update_state(
        root,
        postprocess_required=True,
        current_phase='POSTPROCESS',
        current_status='POSTPROCESS_RUNNING',
        delivery_gate_status='PENDING',
        pending_tasks=['POSTPROCESS_FINALIZER', 'FINAL_DELIVERY'],
    )

    ok, result = validate_existing(root, report)
    if not ok or a.force:
        editable_path = root / 'editable' / 'report-editable.html'
        if editable_path.exists() and not ok:
            # Trace must be written BEFORE the dispatcher overwrites the suspicious
            # artifact; these fields are intentionally not cleared on success so
            # the drift evidence survives the deterministic rebuild.
            missing = [
                p.name for p in (
                    root / 'editable' / 'editor-validation-result.json',
                    root / 'editable' / 'postprocess-status.json',
                ) if not p.exists()
            ]
            update_state(
                root,
                editable_rebuilt_from_invalid=True,
                rebuild_reason=(
                    'pre-existing editable failed delivery validation and was overwritten '
                    'by deterministic rebuild (possible hand-written or stale editable); '
                    'missing=' + (', '.join(missing) if missing else 'none')
                    + '; validation=' + json.dumps(result, ensure_ascii=False)[:800]
                ),
            )
        here = Path(__file__).resolve().parent
        cmd = [
            sys.executable,
            str(here / 'dispatch_postprocess.py'),
            '--input', str(report),
            '--output-root', str(root),
            '--runtime-qa', a.runtime_qa,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        ok, result = validate_existing(root, report)
        if not ok:
            update_state(
                root,
                current_phase='POSTPROCESS',
                current_status='POSTPROCESS_BLOCKED',
                delivery_gate_status='BLOCKED',
                pending_tasks=['POSTPROCESS_FINALIZER', 'FINAL_DELIVERY'],
                postprocess_status=result.get('status', 'FAIL'),
                last_artifact_failure=(result.get('error') or r.stderr or r.stdout or 'postprocess finalizer failed')[:4000],
            )
            payload = {
                'status': 'FAIL',
                'delivery_gate_status': 'BLOCKED',
                'postprocess_result': result,
                'dispatcher_returncode': r.returncode,
                'stdout': r.stdout,
                'stderr': r.stderr,
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2

    # Final deterministic delivery gate.
    current_sha = sha256(report)
    status = result.get('status')
    update_state(
        root,
        postprocess_required=True,
        postprocess_extension_version='Editor Postprocess V2.0 Delivery Gate / Editor Runtime V2.0 (compile-time annotation)',
        postprocess_status=status,
        editable_output_path='editable/report-editable.html',
        editor_validation_result_path='editable/editor-validation-result.json',
        postprocess_status_path='editable/postprocess-status.json',
        delivery_gate_status='PASS',
        current_phase='FINAL_DELIVERY',
        current_status='DELIVERED',
        pending_tasks=[],
        last_artifact_failure=None,
    )
    payload = {
        'status': status,
        'delivery_gate_status': 'PASS',
        'report_html': str(report),
        'editable_html': str(root / 'editable' / 'report-editable.html'),
        'editor_validation_result': str(root / 'editable' / 'editor-validation-result.json'),
        'postprocess_status_path': str(root / 'editable' / 'postprocess-status.json'),
        'base_sha': current_sha,
        'run_state_status': 'DELIVERED',
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
