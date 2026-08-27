#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

BEGIN = '<!-- HE_POSTPROCESS_BEGIN -->'
END = '<!-- HE_POSTPROCESS_END -->'

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build(base: Path, output: Path, css_path: Path, js_path: Path) -> dict:
    if base.resolve() == output.resolve():
        raise SystemExit('Refusing to overwrite base report')
    raw = base.read_bytes()
    before = hashlib.sha256(raw).hexdigest()
    text = raw.decode('utf-8')
    forbidden = [BEGIN, 'id="he-editor-runtime"', 'id="he-editor-meta"', 'id="he-editor-css-template"', 'data-he-edit-id=', 'data-he-module-id=']
    hit = [x for x in forbidden if x in text]
    if hit:
        raise SystemExit(f'Base report already contains Human Editor namespace/markers: {hit}')
    css = css_path.read_text(encoding='utf-8')
    js = js_path.read_text(encoding='utf-8')
    meta = json.dumps({
        'schema_version':'1.0',
        'mode':'deterministic-post-generation-editor',
        'base_report_sha256':before,
        'source_backflow':False,
        'generation_core':'V2.9-FROZEN'
    }, ensure_ascii=False).replace('<','\\u003c')
    block = (
        '\n'+BEGIN+'\n'
        '<template id="he-editor-css-template"><style>'+css+'</style></template>\n'
        '<script type="application/json" id="he-editor-meta">'+meta+'</script>\n'
        '<script id="he-editor-runtime">'+js+'</script>\n'
        +END+'\n'
    )
    m = list(re.finditer(r'</body\s*>', text, flags=re.I))
    if m:
        idx=m[-1].start(); out_text=text[:idx]+block+text[idx:]
    else:
        out_text=text+block
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(out_text, encoding='utf-8')
    after=sha256(base)
    if before != after:
        raise SystemExit('BASE_ARTIFACT_MUTATED')
    return {'base':str(base),'output':str(output),'base_sha256':before,'bytes':output.stat().st_size}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--css')
    p.add_argument('--js')
    args=p.parse_args()
    here=Path(__file__).resolve().parent.parent
    result=build(Path(args.input),Path(args.output),Path(args.css) if args.css else here/'editor'/'editor.css',Path(args.js) if args.js else here/'editor'/'editor.js')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
