#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, shutil
from pathlib import Path
BEGIN='<!-- HE_POSTPROCESS_BEGIN -->'; END='<!-- HE_POSTPROCESS_END -->'

def strip_block(text:str)->str:
    pat=re.compile(r'\n?'+re.escape(BEGIN)+r'.*?'+re.escape(END)+r'\n?',re.S)
    return pat.sub('',text,count=1)

def runtime_html(text:str)->str:
    text=re.sub(r'<link\b[^>]*href=["\']https?://[^>]*>', '', text, flags=re.I)
    text=re.sub(r'<script\b[^>]*src=["\']https?://[^>]*>.*?</script\s*>', '', text, flags=re.I|re.S)
    return text

def browse_equivalence(base_text:str, editable_text:str):
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        return {'status':'SKIPPED','reason':f'playwright unavailable: {e}'}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True, executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
            def probe(text):
                page=browser.new_page(viewport={'width':1440,'height':900})
                page.set_content(runtime_html(text),wait_until='domcontentloaded',timeout=30000)
                page.wait_for_timeout(200)
                data=page.evaluate("""()=>({
                    text:document.body.innerText,
                    scrollHeight:document.documentElement.scrollHeight,
                    scrollWidth:document.documentElement.scrollWidth,
                    bodyWidth:document.body.getBoundingClientRect().width,
                    semanticRects:Array.from(document.querySelectorAll('header,main,section,article,footer')).map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.x*10)/10,Math.round(r.y*10)/10,Math.round(r.width*10)/10,Math.round(r.height*10)/10]})
                })""")
                page.close(); return data
            a=probe(base_text); b=probe(editable_text); browser.close()
        text_equal=a['text']==b['text']; sh_equal=a['scrollHeight']==b['scrollHeight']; sw_equal=a['scrollWidth']==b['scrollWidth']; bw_equal=abs(a['bodyWidth']-b['bodyWidth'])<0.5
        rect_equal=a['semanticRects']==b['semanticRects']
        ok=text_equal and sh_equal and sw_equal and bw_equal and rect_equal
        return {'status':'PASS' if ok else 'FAIL','text_equal':text_equal,'scroll_height_equal':sh_equal,'scroll_width_equal':sw_equal,'body_width_equal':bw_equal,'semantic_rects_equal':rect_equal,'base_geometry':{'scrollHeight':a['scrollHeight'],'scrollWidth':a['scrollWidth'],'bodyWidth':a['bodyWidth']},'editable_geometry':{'scrollHeight':b['scrollHeight'],'scrollWidth':b['scrollWidth'],'bodyWidth':b['bodyWidth']}}
    except Exception as e:
        return {'status':'FAIL','reason':str(e)}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--base',required=True); p.add_argument('--editable',required=True); p.add_argument('--expected-base-sha'); p.add_argument('--static-only', action='store_true')
    a=p.parse_args(); base=Path(a.base); ed=Path(a.editable)
    base_bytes=base.read_bytes(); base_text=base_bytes.decode('utf-8'); ed_text=ed.read_text(encoding='utf-8')
    base_sha=hashlib.sha256(base_bytes).hexdigest()
    checks={
      'expected_base_sha_match': (not a.expected_base_sha) or base_sha==a.expected_base_sha,
      'base_has_no_he_marker': BEGIN not in base_text and 'id="he-editor-runtime"' not in base_text and 'data-he-edit-id=' not in base_text and 'data-he-module-id=' not in base_text,
      'editable_has_begin': BEGIN in ed_text,
      'editable_has_end': END in ed_text,
      'editable_has_runtime': 'id="he-editor-runtime"' in ed_text,
      'editable_has_meta': 'id="he-editor-meta"' in ed_text,
      'editable_has_css_template': 'id="he-editor-css-template"' in ed_text,
      'strip_editor_equals_base': strip_block(ed_text).encode('utf-8')==base_bytes,
    }
    browse={'status':'SKIPPED','reason':'static-only requested'} if a.static_only else browse_equivalence(base_text,ed_text)
    browse_ok=browse.get('status') in ('PASS','SKIPPED')
    status='PASS' if all(checks.values()) and browse_ok else 'FAIL'
    print(json.dumps({'status':status,'base_sha256':base_sha,'checks':checks,'browse_mode_equivalence':browse},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status=='PASS' else 2)
if __name__=='__main__': main()
