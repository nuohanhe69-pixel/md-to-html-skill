#!/usr/bin/env python3
"""M1-4 baseline: deterministic PostProcess delivery chain audit.

Editor V2.0 (compile-time annotation) assertions replace the V1.x
byte-strip check with structural namespace checks:
  - editable carries data-edit-id / module / authority / motion markers
  - base stays free of the whole editor namespace
  - embedded meta ledger matches the base SHA and positive counts
  - hand-written editable drift is still overwritten deterministically
    with a persistent rebuild_reason trace (M1-3)

Scenarios
  happy — fresh output root, run finalizer once, expect all delivery gates PASS.
  drift — simulate Phase 10 execution drift: hand-written editable, missing
          fingerprints, run-state wrongly claims DELIVERED; re-run finalizer
          (what Phase 11 Artifact Reality Check should trigger) and verify the
          deterministic rebuild restores valid delivery with a trace.

Usage
  python tests/postprocess_baseline.py [--workdir DIR] [--keep]
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FINALIZER = SKILL_ROOT / 'postprocess' / 'scripts' / 'finalize_delivery.py'
FIXTURE = Path(__file__).resolve().parent / 'fixtures' / 'report.html'
META_RE = re.compile(r'<script id="human-edit-meta" type="application/json">(.*?)</script>', re.S)

AUTHORITY_MAP = {
    'schema_version': '1.0',
    'targets': [
        {'du': 'DU002', 'contains_text': '关系 R01', 'authority': 'locked-fact', 'obligation_refs': ['C002.R01']},
    ],
    'modules': [
        {'selector': "section[data-du-id='DU003']", 'movable': True},
    ],
}


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
    (root / 'workspace' / 'editable-authority-map.json').write_text(
        json.dumps(AUTHORITY_MAP, ensure_ascii=False, indent=2), encoding='utf-8')
    return root


def run_finalizer(root: Path) -> dict:
    r = subprocess.run(
        [sys.executable, str(FINALIZER), '--output-root', str(root)],
        capture_output=True, text=True, timeout=180,
    )
    try:
        return json.loads(r.stdout)
    except Exception:
        return {'status': 'PARSE_ERROR', 'returncode': r.returncode,
                'stdout': r.stdout[-2000:], 'stderr': r.stderr[-2000:]}


def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def extract_meta(editable_text: str) -> dict:
    m = META_RE.search(editable_text)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except Exception:
        return {}


def gates(root: Path, base_sha: str) -> dict:
    ed = root / 'editable' / 'report-editable.html'
    status = read_json(root / 'editable' / 'postprocess-status.json')
    rs = read_json(root / 'workspace' / 'run-state.json')
    base_text = (root / 'report.html').read_text(encoding='utf-8')
    ed_text = ed.read_text(encoding='utf-8') if ed.exists() else ''
    meta = extract_meta(ed_text)
    base_markers = ('data-edit-id=', 'data-edit-module-id=', 'data-motion-reveal',
                    'human-edit-ledger', 'he-editor-script', 'data-edit-authority')
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
        'editor_v2': {
            'editable_annotated': ed_text.count('data-edit-id=') >= 5,
            'modules_annotated': ed_text.count('data-edit-module-id=') >= 3,
            'runtime_embedded': 'id="he-editor-script"' in ed_text and 'id="human-edit-ledger"' in ed_text,
            'base_unpolluted': not any(m in base_text for m in base_markers),
            'motion_reveal_annotated': 'data-motion-reveal' in ed_text and 'data-motion-reveal' not in base_text,
            'locked_target_present': 'data-edit-authority="locked-fact"' in ed_text,
            'movable_module_present': 'data-edit-movable="true"' in ed_text,
            'meta_sha_matches_base': meta.get('base_report_sha256') == base_sha,
            'meta_counts_positive': bool(meta) and meta.get('editable_elements', 0) > 0
                                    and meta.get('editable_modules', 0) > 0
                                    and meta.get('locked_targets', 0) >= 1
                                    and meta.get('motion_reveal_elements', 0) >= 1,
        },
        'structural_equivalence_pass': (status.get('non_interference') or {}).get('status') == 'PASS',
        'motion_visibility_pass': all(
            (status.get('motion_visibility') or {}).get(k, {}).get('status') == 'PASS'
            for k in ('base', 'editable')),
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

    # Motion gate property checks: the gate verifies the no-JS safety
    # property, not a specific idiom. Both idioms below prove the same
    # property and must PASS; a truly-unsafe page must FAIL.
    motion_dir = work / 'motion'
    motion_dir.mkdir()
    GATE = SKILL_ROOT / 'postprocess' / 'scripts' / 'validate_motion_visibility_safety.py'
    cases = {
        # V1 idiom (V2.9 / GTM.html style): default-hidden + html.no-js fallback
        'idiom-nojs': '''<!DOCTYPE html><html lang="zh" class="no-js"><head><meta charset="UTF-8"><style>
.b-in{opacity:0;transform:translateX(-18px)}
.b-in.on{opacity:1;transform:none}
html.no-js .b-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.b-in{opacity:1;transform:none}}
</style></head><body><section data-du-id="DU001"><p class="b-in">内容</p></section>
<script>document.documentElement.classList.remove('no-js');</script></body></html>''',
        # V2 idiom (report.html style): hidden only under html.motion-ready
        'idiom-conditional': '''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><style>
html.motion-ready .rv{opacity:0;transform:translateY(12px)}
html.motion-ready .rv.rv-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html.motion-ready .rv{opacity:1;transform:none}}
</style></head><body><section data-du-id="DU001"><p class="rv">内容</p></section>
<script>if(!('IntersectionObserver' in window))return;var els=document.querySelectorAll('.rv');</script></body></html>''',
        # Unsafe: hidden with NO fallback proof at all
        'unsafe-no-fallback': '''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><style>
.b-in{opacity:0;transform:translateY(18px)}
.b-in.on{opacity:1;transform:none}
</style></head><body><section data-du-id="DU001"><p class="b-in">内容</p></section>
<script>document.querySelectorAll('.b-in').forEach(e=>e.classList.add('on'));</script></body></html>''',
    }
    out['motion_gate'] = {}
    for name, html_text in cases.items():
        p = motion_dir / f'{name}.html'
        p.write_text(html_text, encoding='utf-8')
        r = subprocess.run([sys.executable, str(GATE), '--html', str(p)],
                           capture_output=True, text=True, timeout=60)
        try:
            d = json.loads(r.stdout)
            out['motion_gate'][name] = {'status': d.get('status'), 'failures': d.get('failures')}
        except Exception:
            out['motion_gate'][name] = {'status': 'PARSE_ERROR', 'failures': [r.stdout[-200:]]}


    # Generation-side boundary violation: the model pre-wrote an editor
    # attribute into the base report. PostProcess must refuse (never repair),
    # block delivery, and leave the base byte-identical.
    contam = make_root(work, 'scenario-contaminated')
    report = contam / 'report.html'
    report.write_text(
        report.read_text(encoding='utf-8').replace(
            '<h2>1 内容链</h2>', '<h2 data-edit-id="PAGE.h2.001">1 内容链</h2>'),
        encoding='utf-8')
    contam_sha = sha(report)
    out['contaminated'] = {
        'finalizer_status': run_finalizer(contam).get('status'),
        'gates': gates(contam, contam_sha),
    }
    rs = read_json(contam / 'workspace' / 'run-state.json')
    out['contaminated']['refusal_recorded'] = 'Artifact Boundary' in (rs.get('last_artifact_failure') or '')

    # Sentinel: module capability silently lost in the editable (module attrs
    # stripped) while the base still carries data-du-id modules — the
    # module_capability_present gate must FAIL.
    sentinel_dir = work / 'sentinel'
    sentinel_dir.mkdir()
    ed = (happy / 'editable' / 'report-editable.html').read_text(encoding='utf-8')
    stripped = re.sub(r'\s+(?:data-edit-module-id|data-edit-movable)="[^"]*"', '', ed)
    (sentinel_dir / 'editable.html').write_text(stripped, encoding='utf-8')
    (sentinel_dir / 'base.html').write_bytes(FIXTURE.read_bytes())
    r = subprocess.run(
        [sys.executable, str(SKILL_ROOT / 'postprocess' / 'scripts' / 'validate_non_interference.py'),
         '--base', str(sentinel_dir / 'base.html'),
         '--editable', str(sentinel_dir / 'editable.html'),
         '--expected-base-sha', base_sha, '--static-only'],
        capture_output=True, text=True, timeout=60)
    try:
        ni = json.loads(r.stdout)
    except Exception:
        ni = {'status': 'PARSE_ERROR', 'stdout': r.stdout[-800:]}
    out['sentinel'] = {
        'status': ni.get('status'),
        'module_capability_present': (ni.get('checks') or {}).get('module_capability_present'),
        'failures': ni.get('failures'),
    }

    happy_gates = out['happy']['gates']
    drift_gates = out['drift']['gates']
    contam_gates = out['contaminated']['gates']
    out['summary'] = {
        'happy_delivery_gate': happy_gates['delivery_gate_status'],
        'drift_recovery_delivery_gate': drift_gates['delivery_gate_status'],
        'base_untouched_all_scenarios': all(
            g['base_sha_unchanged'] for g in (happy_gates, drift_gates, contam_gates)),
        'drift_overwrite_trace_recorded': bool(drift_gates['rebuild_reason_in_run_state']),
        'editor_v2_annotation_ok': all(happy_gates['editor_v2'].values()),
        'editor_v2_recovery_ok': all(drift_gates['editor_v2'].values()),
        'structural_equivalence_pass': happy_gates['structural_equivalence_pass'] and drift_gates['structural_equivalence_pass'],
        'motion_visibility_pass': happy_gates['motion_visibility_pass'] and drift_gates['motion_visibility_pass'],
        'boundary_violation_refused': (
            contam_gates['delivery_gate_status'] == 'BLOCKED'
            and contam_gates['run_state_status'] == 'POSTPROCESS_BLOCKED'
            and out['contaminated']['refusal_recorded']),
        'sentinel_catches_module_loss': (
            out['sentinel']['status'] == 'FAIL'
            and out['sentinel']['module_capability_present'] is False),
        'motion_gate_idiom_neutral': (
            out['motion_gate']['idiom-nojs']['status'] == 'PASS'
            and out['motion_gate']['idiom-conditional']['status'] == 'PASS'
            and out['motion_gate']['unsafe-no-fallback']['status'] == 'FAIL'),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if not a.keep and not a.workdir:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
