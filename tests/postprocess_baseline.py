#!/usr/bin/env python3
"""M1-4 baseline: deterministic PostProcess delivery chain audit.

Scenarios
  happy — fresh output root, run finalizer once, expect all delivery gates PASS.
  drift — simulate Phase 10 execution drift: hand-written editable, missing
          fingerprints, run-state wrongly claims DELIVERED; re-run finalizer
          (what Phase 11 Artifact Reality Check should trigger) and verify the
          deterministic rebuild restores valid delivery.
  isolation (cross-cutting) — base report SHA never changes; editable strips
          back to byte-identical base after removing the injected HE block.

Usage
  python tests/postprocess_baseline.py [--workdir DIR] [--keep]
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FINALIZER = SKILL_ROOT / 'postprocess' / 'scripts' / 'finalize_delivery.py'
FIXTURE = Path(__file__).resolve().parent / 'fixtures' / 'report.html'
HE_BLOCK = re.compile(r'\n?<!-- HE_POSTPROCESS_BEGIN -->.*?<!-- HE_POSTPROCESS_END -->\n?', re.S)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def make_root(base: Path, name: str) -> Path:
    root = base / name
    root.mkdir(parents=True)
    (root / 'report.html').write_bytes(FIXTURE.read_bytes())
    (root / 'workspace').mkdir()
    (root / 'workspace' / 'run-state.json').write_text(json.dumps({
        'current_phase': 'POSTPROCESS',
        'current_status': 'POSTPROCESS_REQUIRED',
        'postprocess_required': True,
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    return root


def run_finalizer(root: Path) -> dict:
    r = subprocess.run(
        [sys.executable, str(FINALIZER), '--output-root', str(root), '--dispatch-mode', 'direct-fallback'],
        capture_output=True, text=True, timeout=180,
    )
    try:
        return json.loads(r.stdout)
    except Exception:
        return {'status': 'PARSE_ERROR', 'returncode': r.returncode,
                'stdout': r.stdout[-2000:], 'stderr': r.stderr[-2000:]}


def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def gates(root: Path, base_sha: str) -> dict:
    ed = root / 'editable' / 'report-editable.html'
    status = read_json(root / 'editable' / 'postprocess-status.json')
    rs = read_json(root / 'workspace' / 'run-state.json')
    stripped_ok = False
    if ed.exists():
        stripped = HE_BLOCK.sub('', ed.read_text(encoding='utf-8'), count=1)
        stripped_ok = stripped.encode('utf-8') == (root / 'report.html').read_bytes()
    return {
        'editable_exists': ed.exists(),
        'result_json_exists': (root / 'editable' / 'editor-validation-result.json').exists(),
        'status_json_exists': (root / 'editable' / 'postprocess-status.json').exists(),
        'postprocess_status': status.get('status'),
        'sha_before_equals_after': status.get('base_sha_before') == status.get('base_sha_after'),
        'sha_matches_base': status.get('base_sha_before') == base_sha,
        'base_sha_unchanged': sha(root / 'report.html') == base_sha,
        'delivery_gate_status': rs.get('delivery_gate_status'),
        'run_state_status': rs.get('current_status'),
        'rebuild_reason_in_run_state': rs.get('rebuild_reason'),
        'strip_editable_equals_base': stripped_ok,
    }


def simulate_drift(root: Path) -> None:
    """Reproduce the observed P1 drift: LLM hand-writes an editable instead of
    running the finalizer — no fingerprints, content loss, stale DELIVERED."""
    ed = root / 'editable' / 'report-editable.html'
    ed.write_text(
        '<!DOCTYPE html><html><body><h1>漂移产物</h1>'
        '<p>LLM 手写的 editable：无指纹、无校验、内容大面积丢失。</p></body></html>',
        encoding='utf-8',
    )
    for f in ('editor-validation-result.json', 'postprocess-status.json'):
        p = root / 'editable' / f
        if p.exists():
            p.unlink()
    rs_path = root / 'workspace' / 'run-state.json'
    rs = read_json(rs_path)
    rs['current_status'] = 'DELIVERED'
    rs['delivery_gate_status'] = 'PASS'
    rs_path.write_text(json.dumps(rs, ensure_ascii=False, indent=2), encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser(description='M1 deterministic postprocess baseline')
    ap.add_argument('--workdir')
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()

    work = Path(a.workdir).resolve() if a.workdir else Path(tempfile.mkdtemp(prefix='md2html-m1-baseline-'))
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    base_sha = sha(FIXTURE)
    out = {'fixture_sha256': base_sha, 'workdir': str(work)}

    happy = make_root(work, 'scenario-happy')
    out['happy'] = {
        'finalizer_status': run_finalizer(happy).get('status'),
        'gates': gates(happy, base_sha),
    }

    drift = make_root(work, 'scenario-drift')
    run_finalizer(drift)
    simulate_drift(drift)
    out['drift'] = {
        'finalizer_status': run_finalizer(drift).get('status'),
        'gates': gates(drift, base_sha),
    }

    out['summary'] = {
        'happy_delivery_gate': out['happy']['gates']['delivery_gate_status'],
        'drift_recovery_delivery_gate': out['drift']['gates']['delivery_gate_status'],
        'base_untouched_all_scenarios': all(
            g['base_sha_unchanged'] and g['strip_editable_equals_base']
            for g in (out['happy']['gates'], out['drift']['gates'])
        ),
        'drift_overwrite_trace_recorded': bool(out['drift']['gates']['rebuild_reason_in_run_state']),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if not a.keep and not a.workdir:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
