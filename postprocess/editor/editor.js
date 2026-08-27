(function(){
  'use strict';
  if(window.__HE_EDITOR_RUNTIME__) return;
  window.__HE_EDITOR_RUNTIME__ = true;

  const META = (()=>{
    try { return JSON.parse(document.getElementById('he-editor-meta')?.textContent || '{}'); }
    catch(_) { return {}; }
  })();
  const cssTemplate = document.getElementById('he-editor-css-template');
  const state = {
    active:false, selected:null, selectedModule:null,
    originals:new Map(), moduleOriginals:new Map(),
    undo:[], redo:[], ledger:[], focusBefore:null
  };

  function uid(prefix, i){ return `${prefix}${String(i).padStart(4,'0')}`; }
  function isEditorNode(el){ return !!(el && (el.closest?.('he-editor-root') || el.id==='he-editor-root')); }
  function hasMeaningfulText(el){ return !!(el.textContent || '').trim(); }
  function safeLeaf(el){
    if(!el || isEditorNode(el)) return false;
    if(!hasMeaningfulText(el)) return false;
    if(el.closest('script,style,noscript,template,svg,canvas')) return false;
    const elementChildren = Array.from(el.children).filter(c=>c.tagName!=='BR');
    return elementChildren.length===0;
  }
  function candidateElements(){
    const selector = 'h1,h2,h3,h4,h5,h6,p,li,th,td,blockquote,figcaption,dt,dd,label,small,span,strong,b,em,i,a';
    return Array.from(document.querySelectorAll(selector)).filter(safeLeaf);
  }
  function moduleElements(){
    const preferred = Array.from(document.querySelectorAll('[data-du],[data-du-id],main > section,main > article,body > section,body > article,header,footer'));
    let mods = preferred.filter(el=>!isEditorNode(el));
    if(!mods.length){
      const main = document.querySelector('main');
      if(main) mods=[main];
    }
    if(!mods.length) mods = Array.from(document.body.children).filter(el=>!isEditorNode(el) && !['SCRIPT','STYLE','TEMPLATE'].includes(el.tagName));
    return Array.from(new Set(mods));
  }
  function discover(){
    moduleElements().forEach((el,i)=>{
      if(!el.hasAttribute('data-he-module-id')) el.setAttribute('data-he-module-id',uid('HE-M',i+1));
      const id=el.getAttribute('data-he-module-id');
      if(!state.moduleOriginals.has(id)) state.moduleOriginals.set(id,{style:el.getAttribute('style')||''});
    });
    candidateElements().forEach((el,i)=>{
      if(!el.hasAttribute('data-he-edit-id')) el.setAttribute('data-he-edit-id',uid('HE-E',i+1));
      const id=el.getAttribute('data-he-edit-id');
      if(!state.originals.has(id)) state.originals.set(id,{html:el.innerHTML,style:el.getAttribute('style')||''});
    });
  }
  function closestModule(el){ return el?.closest?.('[data-he-module-id]') || null; }
  function ident(el){ return el?.getAttribute?.('data-he-edit-id') || el?.getAttribute?.('data-he-module-id') || ''; }
  function elementById(id){
    return document.querySelector(`[data-he-edit-id="${CSS.escape(id)}"],[data-he-module-id="${CSS.escape(id)}"]`);
  }
  function snapshot(el, kind){
    if(!el) return '';
    return kind==='html' ? el.innerHTML : (el.getAttribute('style')||'');
  }
  function setSnapshot(el, kind, value){
    if(kind==='html') el.innerHTML=value;
    else if(value) el.setAttribute('style',value); else el.removeAttribute('style');
  }
  function record(el, kind, before, after, source){
    if(!el || before===after) return;
    const op={id:ident(el),kind,before,after,source:source||'human',ts:new Date().toISOString()};
    state.undo.push(op); state.redo.length=0; state.ledger.push(op); refreshUI();
  }
  function applyOp(op, value){
    const el=elementById(op.id); if(!el) return;
    setSnapshot(el,op.kind,value);
    if(state.selected===el || state.selectedModule===el) syncInspector();
  }
  function undo(){ const op=state.undo.pop(); if(!op) return; applyOp(op,op.before); state.redo.push(op); refreshUI(); }
  function redo(){ const op=state.redo.pop(); if(!op) return; applyOp(op,op.after); state.undo.push(op); refreshUI(); }

  const host=document.createElement('he-editor-root');
  host.id='he-editor-root';
  host.setAttribute('style','all:initial;position:fixed;inset:auto 0 0 auto;z-index:2147483647;pointer-events:none;');
  const shadow=host.attachShadow({mode:'open'});
  if(cssTemplate?.content) shadow.appendChild(cssTemplate.content.cloneNode(true));
  const wrap=document.createElement('div');
  wrap.innerHTML=`
    <button class="he-launcher" id="he-launcher" style="pointer-events:auto">✎ 编辑</button>
    <div class="he-panel" id="he-panel" style="pointer-events:auto">
      <div class="he-head"><div class="he-title">Human Editor</div><span class="he-badge" id="he-count">0 edits</span></div>
      <div class="he-body">
        <div class="he-section">
          <span class="he-label">选择</span><div class="he-value" id="he-selected">未选择元素</div>
          <div class="he-note">进入编辑模式后点击页面中的安全文本叶节点。复杂父容器不会整体 contenteditable。</div>
        </div>
        <div class="he-section">
          <span class="he-label">文字</span><textarea class="he-textarea" id="he-text" disabled></textarea>
          <div class="he-row">
            <div><span class="he-label">字号</span><input class="he-input" id="he-font-size" placeholder="如 16px"></div>
            <div><span class="he-label">字重</span><select class="he-select" id="he-font-weight"><option value="">保持</option><option>400</option><option>500</option><option>600</option><option>700</option><option>800</option><option>900</option></select></div>
          </div>
          <div class="he-row">
            <div><span class="he-label">颜色</span><input class="he-input" id="he-color" placeholder="#111 / var(...) "></div>
            <div><span class="he-label">对齐</span><select class="he-select" id="he-align"><option value="">保持</option><option value="left">left</option><option value="center">center</option><option value="right">right</option><option value="justify">justify</option></select></div>
          </div>
          <div class="he-actions"><button class="he-btn" id="he-reset-el">重置元素</button></div>
        </div>
        <div class="he-section">
          <span class="he-label">模块</span><div class="he-value" id="he-module">未识别模块</div>
          <div class="he-row"><input class="he-input" id="he-mt" placeholder="margin-top"><input class="he-input" id="he-mb" placeholder="margin-bottom"></div>
          <div class="he-row"><input class="he-input" id="he-pt" placeholder="padding-top"><input class="he-input" id="he-pb" placeholder="padding-bottom"></div>
          <div class="he-row"><input class="he-input" id="he-width" placeholder="max-width"><input class="he-input" id="he-bg" placeholder="background"></div>
          <div class="he-row one"><input class="he-input" id="he-border" placeholder="border，如 1px solid #ddd"></div>
          <div class="he-actions"><button class="he-btn" id="he-reset-mod">重置模块样式</button></div>
        </div>
        <div class="he-section">
          <div class="he-actions">
            <button class="he-btn" id="he-undo">撤销</button><button class="he-btn" id="he-redo">重做</button>
            <button class="he-btn danger" id="he-reset-all">全部重置</button>
          </div>
          <div class="he-actions">
            <button class="he-btn primary" id="he-save">保存可编辑版</button>
            <button class="he-btn" id="he-publish">导出发布版</button>
            <button class="he-btn" id="he-ledger">导出台账</button>
          </div>
          <div class="he-status" id="he-status">浏览模式：原报告行为保持不变。</div>
        </div>
      </div>
    </div>`;
  while(wrap.firstChild) shadow.appendChild(wrap.firstChild);
  document.body.appendChild(host);

  const $=id=>shadow.getElementById(id);
  const launcher=$('he-launcher'), panel=$('he-panel'), selectedLabel=$('he-selected'), moduleLabel=$('he-module'), status=$('he-status');

  function setSelected(el){
    if(state.selected && state.selected!==el){ state.selected.removeAttribute('data-he-selected'); state.selected.removeAttribute('contenteditable'); }
    state.selected=el; state.selectedModule=closestModule(el);
    if(el){
      el.setAttribute('data-he-selected','true');
      if(safeLeaf(el)) el.setAttribute('contenteditable','true');
    }
    syncInspector();
  }
  function syncInspector(){
    const el=state.selected, mod=state.selectedModule;
    selectedLabel.textContent=el ? `${el.tagName.toLowerCase()} · ${ident(el)}` : '未选择元素';
    moduleLabel.textContent=mod ? `${mod.tagName.toLowerCase()} · ${ident(mod)}` : '未识别模块';
    const text=$('he-text'); text.disabled=!el; text.value=el ? el.textContent : '';
    $('he-font-size').value=el?.style?.fontSize||''; $('he-font-weight').value=el?.style?.fontWeight||'';
    $('he-color').value=el?.style?.color||''; $('he-align').value=el?.style?.textAlign||'';
    $('he-mt').value=mod?.style?.marginTop||''; $('he-mb').value=mod?.style?.marginBottom||'';
    $('he-pt').value=mod?.style?.paddingTop||''; $('he-pb').value=mod?.style?.paddingBottom||'';
    $('he-width').value=mod?.style?.maxWidth||''; $('he-bg').value=mod?.style?.background||''; $('he-border').value=mod?.style?.border||'';
  }
  function refreshUI(){
    $('he-count').textContent=`${state.ledger.length} edits`;
    $('he-undo').disabled=!state.undo.length; $('he-redo').disabled=!state.redo.length;
  }
  function enter(){
    discover(); state.active=true; panel.classList.add('open'); launcher.textContent='✓ 完成编辑';
    status.textContent='编辑模式：点击安全文本叶节点直接修改；编辑器不控制原页面 Motion / Scroll / Navigation。';
  }
  function exit(){
    state.active=false; if(state.selected){state.selected.removeAttribute('contenteditable'); state.selected.removeAttribute('data-he-selected');}
    state.selected=null; state.selectedModule=null; panel.classList.remove('open'); launcher.textContent='✎ 编辑';
    status.textContent='浏览模式：原报告行为保持不变。'; syncInspector();
  }
  launcher.addEventListener('click',()=> state.active ? exit() : enter());

  document.addEventListener('click',e=>{
    if(!state.active || isEditorNode(e.target)) return;
    const el=e.target.closest?.('[data-he-edit-id]');
    if(!el) return;
    if(el.tagName==='A') e.preventDefault();
    setSelected(el);
  },true);
  document.addEventListener('focusin',e=>{
    if(!state.active) return;
    const el=e.target.closest?.('[data-he-edit-id]');
    if(el && el===state.selected) state.focusBefore=el.innerHTML;
  },true);
  document.addEventListener('focusout',e=>{
    const el=e.target.closest?.('[data-he-edit-id]');
    if(el && state.focusBefore!==null){ const after=el.innerHTML; record(el,'html',state.focusBefore,after,'direct-text'); state.focusBefore=null; syncInspector(); }
  },true);

  function bindStyle(id, prop, module=false){
    $(id).addEventListener('change',e=>{
      const el=module ? state.selectedModule : state.selected; if(!el) return;
      const before=snapshot(el,'style'); el.style[prop]=e.target.value; const after=snapshot(el,'style');
      record(el,'style',before,after,module?'module-style':'element-style');
    });
  }
  $('he-text').addEventListener('change',e=>{
    const el=state.selected; if(!el) return;
    const before=el.innerHTML;
    el.textContent=e.target.value;
    const after=el.innerHTML; record(el,'html',before,after,'inspector-text');
  });
  bindStyle('he-font-size','fontSize'); bindStyle('he-font-weight','fontWeight'); bindStyle('he-color','color'); bindStyle('he-align','textAlign');
  bindStyle('he-mt','marginTop',true); bindStyle('he-mb','marginBottom',true); bindStyle('he-pt','paddingTop',true); bindStyle('he-pb','paddingBottom',true);
  bindStyle('he-width','maxWidth',true); bindStyle('he-bg','background',true); bindStyle('he-border','border',true);
  $('he-undo').addEventListener('click',undo); $('he-redo').addEventListener('click',redo);

  $('he-reset-el').addEventListener('click',()=>{
    const el=state.selected; if(!el) return; const o=state.originals.get(ident(el)); if(!o) return;
    const beforeHtml=el.innerHTML, beforeStyle=snapshot(el,'style'); el.innerHTML=o.html; setSnapshot(el,'style',o.style);
    record(el,'html',beforeHtml,o.html,'reset-element'); if(beforeStyle!==o.style) record(el,'style',beforeStyle,o.style,'reset-element'); syncInspector();
  });
  $('he-reset-mod').addEventListener('click',()=>{
    const mod=state.selectedModule; if(!mod) return; const o=state.moduleOriginals.get(ident(mod)); if(!o) return;
    const before=snapshot(mod,'style'); setSnapshot(mod,'style',o.style); record(mod,'style',before,o.style,'reset-module'); syncInspector();
  });
  $('he-reset-all').addEventListener('click',()=>{
    if(!window.confirm('确认重置本次人工编辑？')) return;
    state.originals.forEach((o,id)=>{const el=elementById(id); if(el){el.innerHTML=o.html; setSnapshot(el,'style',o.style);}});
    state.moduleOriginals.forEach((o,id)=>{const el=elementById(id); if(el)setSnapshot(el,'style',o.style);});
    state.undo.length=0; state.redo.length=0; state.ledger.push({kind:'reset-all',ts:new Date().toISOString()}); refreshUI(); syncInspector();
  });

  function cleanEphemeral(root, removeRuntime){
    root.querySelectorAll('[contenteditable]').forEach(el=>el.removeAttribute('contenteditable'));
    root.querySelectorAll('[data-he-selected]').forEach(el=>el.removeAttribute('data-he-selected'));
    root.querySelectorAll('he-editor-root').forEach(el=>el.remove());
    if(removeRuntime){
      root.querySelectorAll('[data-he-edit-id],[data-he-module-id]').forEach(el=>{el.removeAttribute('data-he-edit-id');el.removeAttribute('data-he-module-id');});
      ['he-editor-css-template','he-editor-meta','he-editor-runtime'].forEach(id=>root.getElementById(id)?.remove());
      const walker=document.createTreeWalker(root,NodeFilter.SHOW_COMMENT); const rm=[]; while(walker.nextNode()){ if((walker.currentNode.nodeValue||'').includes('HE_POSTPROCESS_')) rm.push(walker.currentNode); } rm.forEach(n=>n.remove());
    }
  }
  function serialize(clone){ return '<!DOCTYPE html>\n'+clone.documentElement.outerHTML; }
  function download(name, text, type){
    const blob=new Blob([text],{type:type||'text/html;charset=utf-8'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click();
    setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);
  }
  $('he-save').addEventListener('click',()=>{
    const clone=document.cloneNode(true); cleanEphemeral(clone,false); download('report-editable.html',serialize(clone)); status.textContent='已导出可继续编辑的 HTML。';
  });
  $('he-publish').addEventListener('click',()=>{
    const clone=document.cloneNode(true); cleanEphemeral(clone,true); download('report-published.html',serialize(clone)); status.textContent='已导出干净发布版 HTML。';
  });
  $('he-ledger').addEventListener('click',()=>{
    download('human-edit-ledger.json',JSON.stringify({schema:'he-ledger-v1',base_sha256:META.base_report_sha256||'',exported_at:new Date().toISOString(),edits:state.ledger},null,2),'application/json');
  });
  document.addEventListener('keydown',e=>{
    if(!state.active || e.target?.isContentEditable) return;
    if((e.metaKey||e.ctrlKey)&&!e.shiftKey&&e.key.toLowerCase()==='z'){e.preventDefault();undo();}
    if(((e.metaKey||e.ctrlKey)&&e.shiftKey&&e.key.toLowerCase()==='z')||(e.ctrlKey&&e.key.toLowerCase()==='y')){e.preventDefault();redo();}
  });

  refreshUI(); syncInspector();
})();
