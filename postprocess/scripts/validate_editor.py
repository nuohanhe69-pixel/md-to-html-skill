#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, shutil, subprocess
from pathlib import Path

FORBIDDEN = [
  'IntersectionObserver','animationTimeline','scrollTimeline','motion-ready','data-motion-reveal',
  "classList.add('on')",'classList.add("on")',"classList.add('in')",'classList.add("in")',
  "querySelectorAll('.rv')",'querySelectorAll(".rv")',"querySelectorAll('.reveal')",'querySelectorAll(".reveal")'
]

def static_validate(html:Path, js:Path):
    text=html.read_text(encoding='utf-8'); js_text=js.read_text(encoding='utf-8')
    checks={
      'runtime_marker': 'id="he-editor-runtime"' in text,
      'meta_marker': 'id="he-editor-meta"' in text,
      'shadow_css_template': 'id="he-editor-css-template"' in text,
      'js_no_forbidden_motion_coupling': not any(t in js_text for t in FORBIDDEN),
      'js_uses_shadow_dom': 'attachShadow' in js_text,
      'js_no_llm': not re.search(r'openai|anthropic|gemini|llm|huashu',js_text,re.I),
    }
    node='SKIPPED'
    if shutil.which('node'):
      r=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
      node='PASS' if r.returncode==0 else 'FAIL: '+(r.stderr.strip() or r.stdout.strip())
      checks['node_syntax']=r.returncode==0
    return checks,node

def runtime_validate(path:Path):
    try:
      from playwright.sync_api import sync_playwright
    except Exception as e:
      return {'status':'SKIPPED','reason':f'playwright unavailable: {e}'}
    try:
      with sync_playwright() as p:
        browser=p.chromium.launch(headless=True, executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':900})
        html_text=path.read_text(encoding='utf-8')
        # Runtime probe only: remove external HTTP assets so set_content cannot be blocked by network policy.
        html_text=re.sub(r'<link\b[^>]*href=[\"\']https?://[^>]*>', '', html_text, flags=re.I)
        html_text=re.sub(r'<script\b[^>]*src=[\"\']https?://[^>]*>.*?</script\s*>', '', html_text, flags=re.I|re.S)
        page.set_content(html_text,wait_until='domcontentloaded',timeout=30000)
        page.wait_for_timeout(250)
        host=page.locator('he-editor-root')
        if host.count()!=1: raise RuntimeError('editor host missing')
        # Enter edit mode through shadow root.
        page.evaluate("document.querySelector('he-editor-root').shadowRoot.getElementById('he-launcher').click()")
        page.wait_for_timeout(120)
        discovered=page.locator('[data-he-edit-id]').count(); modules=page.locator('[data-he-module-id]').count()
        whole_modules=page.locator('[data-he-module-id][contenteditable="true"]').count()
        if discovered<1: raise RuntimeError('no editable leaf discovered')
        if whole_modules!=0: raise RuntimeError('whole module contenteditable detected')
        # Pick first editable leaf and exercise inspector text + undo/redo.
        first=page.locator('[data-he-edit-id]').first
        eid=first.get_attribute('data-he-edit-id'); before=first.text_content() or ''
        page.evaluate("id=>document.querySelector('[data-he-edit-id=\"'+id+'\"]').click()",eid)
        page.evaluate("v=>{const s=document.querySelector('he-editor-root').shadowRoot; const t=s.getElementById('he-text'); t.value=v; t.dispatchEvent(new Event('change',{bubbles:true}));}", before+'__HE_TEST__')
        changed=first.text_content() or ''
        page.evaluate("document.querySelector('he-editor-root').shadowRoot.getElementById('he-undo').click()")
        undone=first.text_content() or ''
        page.evaluate("document.querySelector('he-editor-root').shadowRoot.getElementById('he-redo').click()")
        redone=first.text_content() or ''
        browser.close()
        ok=('__HE_TEST__' in changed and undone==before and '__HE_TEST__' in redone)
        return {'status':'PASS' if ok else 'FAIL','editable_elements':discovered,'modules':modules,'whole_module_contenteditable':whole_modules,'text_edit': '__HE_TEST__' in changed,'undo':undone==before,'redo':'__HE_TEST__' in redone}
    except Exception as e:
      return {'status':'FAIL','reason':str(e)}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--html',required=True); p.add_argument('--js'); p.add_argument('--static-only', action='store_true')
    a=p.parse_args(); html=Path(a.html); js=Path(a.js) if a.js else Path(__file__).resolve().parent.parent/'editor'/'editor.js'
    checks,node=static_validate(html,js); runtime={'status':'SKIPPED','reason':'static-only requested'} if a.static_only else runtime_validate(html)
    static_ok=all(checks.values()); runtime_ok=runtime.get('status') in ('PASS','SKIPPED')
    status='PASS' if static_ok and runtime_ok else 'FAIL'
    print(json.dumps({'status':status,'static_checks':checks,'node_syntax':node,'runtime':runtime},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status=='PASS' else 2)
if __name__=='__main__': main()
