(function(){
  'use strict';
  if (window.__humanEditLayerInitialized) return;
  window.__humanEditLayerInitialized = true;

  var doc = document;
  var body = doc.body;
  var ledgerNode = doc.getElementById('human-edit-ledger');
  var baseNode = doc.getElementById('human-edit-base-state');
  if (!ledgerNode || !baseNode) return;

  function parseJSON(node, fallback){
    try { return JSON.parse(node.textContent || ''); } catch(e) { return fallback; }
  }
  var ledger = parseJSON(ledgerNode, {schema_version:'1.0', history:[], cursor:-1});
  var baseState = parseJSON(baseNode, {elements:{}, modules:{}});
  if (!Array.isArray(ledger.history)) ledger.history=[];
  if (typeof ledger.cursor !== 'number') ledger.cursor=ledger.history.length-1;

  var state = {
    editing:false,
    selectedElement:null,
    selectedModule:null,
    focusBefore:null,
    suppress:false
  };

  function el(tag, attrs, text){
    var n=doc.createElement(tag);
    Object.keys(attrs||{}).forEach(function(k){
      if (k==='class') n.className=attrs[k]; else n.setAttribute(k, attrs[k]);
    });
    if (text != null) n.textContent=text;
    return n;
  }

  function addOption(select, value, label){
    var o=doc.createElement('option'); o.value=value; o.textContent=label; select.appendChild(o);
  }

  var launcher=el('button',{id:'he-launcher','data-he-runtime-ui':'1',type:'button'},'✎ 编辑页面');
  var toolbar=el('div',{id:'he-toolbar','data-he-runtime-ui':'1',role:'toolbar','aria-label':'人工编辑工具栏'});
  var title=el('span',{class:'he-title'},'EDIT MODE');
  var status=el('span',{class:'he-status'},'未选择内容');
  var undoBtn=el('button',{id:'he-undo',type:'button'},'撤销');
  var redoBtn=el('button',{id:'he-redo',type:'button'},'重做');
  var resetElBtn=el('button',{id:'he-reset-el',type:'button'},'恢复元素');
  var resetModBtn=el('button',{id:'he-reset-mod',type:'button'},'恢复模块');
  var resetPageBtn=el('button',{id:'he-reset-page',type:'button',class:'he-danger'},'恢复全部');
  var exportEditableBtn=el('button',{id:'he-export-editable',type:'button',class:'he-primary'},'保存可编辑版本');
  var exportCleanBtn=el('button',{id:'he-export-clean',type:'button'},'导出发布版');
  var exportPatchBtn=el('button',{id:'he-export-ledger',type:'button'},'导出修改记录');
  var exitBtn=el('button',{id:'he-exit',type:'button'},'退出编辑');
  [title,status,undoBtn,redoBtn,resetElBtn,resetModBtn,resetPageBtn,exportEditableBtn,exportCleanBtn,exportPatchBtn,exitBtn].forEach(function(n){toolbar.appendChild(n);});

  var panel=el('aside',{id:'he-panel','data-he-runtime-ui':'1','aria-label':'编辑面板'});
  panel.innerHTML='\
    <div class="he-panel-head">\
      <div class="he-kicker">CURRENT SELECTION</div>\
      <div class="he-selection" id="he-selection">未选择</div>\
      <div class="he-authority" id="he-authority">—</div>\
    </div>\
    <div class="he-section" id="he-element-section">\
      <h4>元素编辑</h4>\
      <label>文字<textarea id="he-text" disabled></textarea></label>\
      <div class="he-grid">\
        <label>字号<select id="he-font-size"></select></label>\
        <label>字重<select id="he-font-weight"></select></label>\
        <label>对齐<select id="he-align"></select></label>\
        <label>文字颜色<input id="he-color" type="color" value="#111827"></label>\
      </div>\
      <div class="he-actions"><button type="button" id="he-apply-text" class="he-primary">应用文字</button></div>\
      <p class="he-note">文本也可在页面中直接点击后编辑。Locked Content 会在首次修改前要求人工确认。</p>\
    </div>\
    <div class="he-section">\
      <h4>模块样式</h4>\
      <div class="he-grid">\
        <label>上间距<select id="he-mt"></select></label>\
        <label>下间距<select id="he-mb"></select></label>\
        <label>上内边距<select id="he-pt"></select></label>\
        <label>下内边距<select id="he-pb"></select></label>\
      </div>\
      <label>宽度<select id="he-width"></select></label>\
      <label>布局<select id="he-layout"></select></label>\
      <div class="he-grid">\
        <label>背景色<input id="he-bg" type="color" value="#ffffff"></label>\
        <label>边框<select id="he-border"></select></label>\
      </div>\
      <div class="he-actions">\
        <button type="button" id="he-move-up">↑ 上移</button>\
        <button type="button" id="he-move-down">↓ 下移</button>\
      </div>\
      <p class="he-note" id="he-move-note">仅显式标记为可安全移动的模块开放顺序调整。</p>\
    </div>';

  var confirm=el('div',{id:'he-confirm','data-he-runtime-ui':'1','aria-hidden':'true'});
  confirm.innerHTML='\
    <div class="he-confirm-card" role="dialog" aria-modal="true" aria-labelledby="he-confirm-title">\
      <h3 id="he-confirm-title">⚠ Human Override</h3>\
      <p id="he-confirm-text">该字段属于锁定内容。人工仍可修改，但此操作会记录为 Human Override；不会回写 Markdown、DIP 或其他上游材料。</p>\
      <div class="he-confirm-actions"><button type="button" id="he-confirm-cancel">取消</button><button type="button" id="he-confirm-ok" class="he-primary">继续修改</button></div>\
    </div>';

  body.appendChild(launcher); body.appendChild(toolbar); body.appendChild(panel); body.appendChild(confirm);

  var q=function(s){return doc.querySelector(s);};
  var controls={
    sel:q('#he-selection'), auth:q('#he-authority'), text:q('#he-text'), applyText:q('#he-apply-text'),
    fontSize:q('#he-font-size'), fontWeight:q('#he-font-weight'), align:q('#he-align'), color:q('#he-color'),
    mt:q('#he-mt'), mb:q('#he-mb'), pt:q('#he-pt'), pb:q('#he-pb'), width:q('#he-width'), layout:q('#he-layout'),
    bg:q('#he-bg'), border:q('#he-border'), moveUp:q('#he-move-up'), moveDown:q('#he-move-down'), moveNote:q('#he-move-note')
  };

  [['','继承'],['12px','12'],['14px','14'],['16px','16'],['18px','18'],['20px','20'],['24px','24'],['28px','28'],['32px','32'],['40px','40'],['48px','48'],['64px','64']].forEach(function(x){addOption(controls.fontSize,x[0],x[1]);});
  [['','继承'],['400','Regular'],['500','Medium'],['600','SemiBold'],['700','Bold'],['800','ExtraBold'],['900','Black']].forEach(function(x){addOption(controls.fontWeight,x[0],x[1]);});
  [['','继承'],['left','左'],['center','中'],['right','右']].forEach(function(x){addOption(controls.align,x[0],x[1]);});
  ['', '0px','8px','16px','24px','32px','48px','64px','96px'].forEach(function(v){addOption(controls.mt,v,v||'继承');addOption(controls.mb,v,v||'继承');addOption(controls.pt,v,v||'继承');addOption(controls.pb,v,v||'继承');});
  [['','当前'],['720px','窄'],['960px','正文'],['1200px','宽'],['100%','满宽']].forEach(function(x){addOption(controls.width,x[0],x[1]);});
  [['current','当前布局'],['single','单列'],['two','双列'],['row','横向排列'],['column','纵向排列']].forEach(function(x){addOption(controls.layout,x[0],x[1]);});
  [['','当前'],['0','无'],['1px solid currentColor','1px'],['2px solid currentColor','2px']].forEach(function(x){addOption(controls.border,x[0],x[1]);});

  function authorityOf(node){ return node && (node.getAttribute('data-edit-authority') || 'human-editable'); }
  function isLocked(node){ var a=authorityOf(node); return a !== 'human-editable' && a !== 'free'; }
  function moduleFor(node){ return node ? node.closest('[data-edit-module-id]') : null; }

  function cleanSelection(){
    doc.querySelectorAll('.he-selected-element').forEach(function(n){n.classList.remove('he-selected-element');});
    doc.querySelectorAll('.he-selected-module').forEach(function(n){n.classList.remove('he-selected-module');});
  }

  function ensureTag(mod){
    if (!mod) return;
    var tag=mod.querySelector(':scope > .he-module-tag');
    if (!tag){ tag=el('span',{class:'he-module-tag','data-he-runtime-ui':'1'},mod.getAttribute('data-edit-module-id')); mod.insertBefore(tag,mod.firstChild); }
    tag.textContent=mod.getAttribute('data-edit-module-id');
  }

  function selectNode(node){
    if (!state.editing) return;
    cleanSelection();
    state.selectedElement=node && node.hasAttribute('data-edit-id') ? node : null;
    state.selectedModule=moduleFor(node) || (node && node.hasAttribute('data-edit-module-id') ? node : null);
    if (state.selectedElement) state.selectedElement.classList.add('he-selected-element');
    if (state.selectedModule){ state.selectedModule.classList.add('he-selected-module'); ensureTag(state.selectedModule); }
    refreshPanel();
  }

  function refreshPanel(){
    var e=state.selectedElement, m=state.selectedModule;
    var name=e ? e.getAttribute('data-edit-id') : (m ? m.getAttribute('data-edit-module-id') : '未选择');
    controls.sel.textContent=name;
    var auth=e ? authorityOf(e) : (m ? authorityOf(m) : '—');
    controls.auth.textContent=auth;
    controls.auth.classList.toggle('warn', !!(e && isLocked(e)));
    controls.text.disabled=!e;
    controls.applyText.disabled=!e;
    controls.text.value=e ? e.textContent : '';
    controls.fontSize.disabled=controls.fontWeight.disabled=controls.align.disabled=controls.color.disabled=!e;
    if(e){
      controls.fontSize.value=e.style.fontSize||'';
      controls.fontWeight.value=e.style.fontWeight||'';
      controls.align.value=e.style.textAlign||'';
      controls.color.value=toHex(getComputedStyle(e).color) || '#111827';
    }
    [controls.mt,controls.mb,controls.pt,controls.pb,controls.width,controls.layout,controls.bg,controls.border].forEach(function(c){c.disabled=!m;});
    controls.moveUp.disabled=controls.moveDown.disabled=!(m && m.getAttribute('data-edit-movable')==='true');
    controls.moveNote.textContent=(m && m.getAttribute('data-edit-movable')==='true') ? '移动会记录为 Human Override，仅改变最终产物叙事顺序。' : '该模块未标记为可安全移动；为保护 DOM / 响应式结构，顺序按钮已禁用。';
    if(m){
      controls.mt.value=m.style.marginTop||''; controls.mb.value=m.style.marginBottom||'';
      controls.pt.value=m.style.paddingTop||''; controls.pb.value=m.style.paddingBottom||'';
      controls.width.value=m.style.maxWidth||'';
      controls.bg.value=toHex(getComputedStyle(m).backgroundColor) || '#ffffff';
      controls.border.value=m.style.border||'';
      controls.layout.value='current';
    }
    updateButtons();
  }

  function toHex(rgb){
    var m=(rgb||'').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/); if(!m) return null;
    return '#'+[m[1],m[2],m[3]].map(function(x){return Number(x).toString(16).padStart(2,'0');}).join('');
  }

  function confirmOverride(node, cb){
    if (!isLocked(node)) { cb(); return; }
    confirm.classList.add('he-open'); confirm.setAttribute('aria-hidden','false');
    var t=q('#he-confirm-text');
    t.textContent='该字段属于 '+authorityOf(node)+'。人工仍可修改，但会记录为 Human Override；不会回写 Markdown、Source Inventory、DIP、Design Intent 或其他上游材料。';
    var ok=q('#he-confirm-ok'), cancel=q('#he-confirm-cancel');
    function done(yes){ ok.removeEventListener('click',yesFn); cancel.removeEventListener('click',noFn); confirm.classList.remove('he-open'); confirm.setAttribute('aria-hidden','true'); if(yes) cb(); }
    function yesFn(){done(true);} function noFn(){done(false);}
    ok.addEventListener('click',yesFn); cancel.addEventListener('click',noFn);
  }

  function opTarget(op){
    if(op.target_type==='element') return doc.querySelector('[data-edit-id="'+cssEsc(op.target)+'"]');
    return doc.querySelector('[data-edit-module-id="'+cssEsc(op.target)+'"]');
  }
  function cssEsc(v){ return window.CSS && CSS.escape ? CSS.escape(v) : String(v).replace(/"/g,'\\"'); }

  function commit(op, alreadyApplied){
    if(state.suppress) return;
    if(ledger.cursor < ledger.history.length-1) ledger.history=ledger.history.slice(0,ledger.cursor+1);
    op.patch_id='HE-'+String(ledger.history.length+1).padStart(4,'0');
    op.timestamp=new Date().toISOString();
    ledger.history.push(op); ledger.cursor=ledger.history.length-1;
    if(!alreadyApplied) applyOp(op,true);
    syncLedger(); updateButtons(); refreshPanel();
  }

  function applyOp(op, forward){
    var n=opTarget(op); if(!n) return;
    state.suppress=true;
    var v=forward?op.after:op.before;
    if(op.operation==='text_replace') n.textContent=v;
    else if(op.operation==='style_change') n.style.setProperty(op.property,v||'');
    else if(op.operation==='style_attr') { if(v) n.setAttribute('style',v); else n.removeAttribute('style'); }
    else if(op.operation==='move_module') moveToIndex(n, v);
    state.suppress=false;
  }

  function moveToIndex(node, index){
    var p=node.parentElement; if(!p) return;
    var sibs=Array.prototype.filter.call(p.children,function(x){return x.hasAttribute && x.hasAttribute('data-edit-module-id');});
    index=Math.max(0,Math.min(Number(index)||0,sibs.length-1));
    var ref=sibs[index];
    if(ref===node) return;
    if(sibs.indexOf(node)<index) p.insertBefore(node,ref.nextSibling); else p.insertBefore(node,ref);
  }

  function currentModuleIndex(m){
    if(!m||!m.parentElement) return -1;
    return Array.prototype.filter.call(m.parentElement.children,function(x){return x.hasAttribute&&x.hasAttribute('data-edit-module-id');}).indexOf(m);
  }

  function syncLedger(){
    ledger.effective_patches=ledger.history.slice(0,ledger.cursor+1);
    ledger.updated_at=new Date().toISOString();
    ledgerNode.textContent=JSON.stringify(ledger,null,2);
  }

  function updateButtons(){
    undoBtn.disabled=ledger.cursor<0;
    redoBtn.disabled=ledger.cursor>=ledger.history.length-1;
    resetElBtn.disabled=!state.selectedElement;
    resetModBtn.disabled=!state.selectedModule;
  }

  function undo(){ if(ledger.cursor<0)return; var op=ledger.history[ledger.cursor]; applyOp(op,false); ledger.cursor--; syncLedger(); refreshPanel(); }
  function redo(){ if(ledger.cursor>=ledger.history.length-1)return; ledger.cursor++; applyOp(ledger.history[ledger.cursor],true); syncLedger(); refreshPanel(); }

  function setEditing(on){
    state.editing=!!on;
    body.classList.toggle('he-editing',state.editing);
    doc.querySelectorAll('[data-edit-id]').forEach(function(n){
      if(state.editing && n.getAttribute('data-edit-type')==='text') n.setAttribute('contenteditable','true');
      else n.removeAttribute('contenteditable');
      n.setAttribute('spellcheck','false');
    });
    if(!state.editing){ cleanSelection(); state.selectedElement=null; state.selectedModule=null; }
    refreshPanel();
  }

  launcher.addEventListener('click',function(){setEditing(true);});
  exitBtn.addEventListener('click',function(){setEditing(false);});
  undoBtn.addEventListener('click',undo); redoBtn.addEventListener('click',redo);

  doc.addEventListener('click',function(e){
    if(!state.editing) return;
    if(e.target.closest('[data-he-runtime-ui]')) return;
    var editable=e.target.closest('[data-edit-id]');
    var mod=e.target.closest('[data-edit-module-id]');
    if(editable || mod){ e.preventDefault(); e.stopPropagation(); }
    if(editable) selectNode(editable); else if(mod) selectNode(mod);
  },true);

  doc.addEventListener('focusin',function(e){
    if(!state.editing || !e.target.hasAttribute('data-edit-id')) return;
    state.focusBefore=e.target.textContent;
    selectNode(e.target);
  });
  doc.addEventListener('focusout',function(e){
    if(!state.editing || !e.target.hasAttribute('data-edit-id') || state.focusBefore==null) return;
    var node=e.target, before=state.focusBefore, after=node.textContent; state.focusBefore=null;
    if(before===after) return;
    // Undo the direct browser edit until authority is confirmed, then replay as a tracked patch.
    node.textContent=before;
    confirmOverride(node,function(){
      node.textContent=after;
      commit({target_type:'element',target:node.getAttribute('data-edit-id'),operation:'text_replace',before:before,after:after,authority:authorityOf(node),scope:isLocked(node)?'HUMAN_OVERRIDE':'HUMAN_EDIT'},true);
    });
  });

  controls.applyText.addEventListener('click',function(){
    var n=state.selectedElement; if(!n)return; var before=n.textContent, after=controls.text.value; if(before===after)return;
    confirmOverride(n,function(){ commit({target_type:'element',target:n.getAttribute('data-edit-id'),operation:'text_replace',before:before,after:after,authority:authorityOf(n),scope:isLocked(n)?'HUMAN_OVERRIDE':'HUMAN_EDIT'}); });
  });

  function bindElementStyle(control, prop){
    control.addEventListener('change',function(){
      var n=state.selectedElement; if(!n)return; var before=n.style.getPropertyValue(prop), after=control.value;
      if(before===after)return; confirmOverride(n,function(){ commit({target_type:'element',target:n.getAttribute('data-edit-id'),operation:'style_change',property:prop,before:before,after:after,authority:authorityOf(n),scope:isLocked(n)?'HUMAN_OVERRIDE':'HUMAN_EDIT'}); });
    });
  }
  bindElementStyle(controls.fontSize,'font-size'); bindElementStyle(controls.fontWeight,'font-weight'); bindElementStyle(controls.align,'text-align');
  controls.color.addEventListener('change',function(){ var n=state.selectedElement;if(!n)return;var b=n.style.color||'',a=controls.color.value;confirmOverride(n,function(){commit({target_type:'element',target:n.getAttribute('data-edit-id'),operation:'style_change',property:'color',before:b,after:a,authority:authorityOf(n),scope:isLocked(n)?'HUMAN_OVERRIDE':'HUMAN_EDIT'});});});

  function bindModuleStyle(control, prop){
    control.addEventListener('change',function(){ var n=state.selectedModule;if(!n)return;var b=n.style.getPropertyValue(prop),a=control.value;if(b===a)return;commit({target_type:'module',target:n.getAttribute('data-edit-module-id'),operation:'style_change',property:prop,before:b,after:a,authority:'HUMAN',scope:'HOW_OVERRIDE'}); });
  }
  bindModuleStyle(controls.mt,'margin-top'); bindModuleStyle(controls.mb,'margin-bottom'); bindModuleStyle(controls.pt,'padding-top'); bindModuleStyle(controls.pb,'padding-bottom');
  controls.width.addEventListener('change',function(){var n=state.selectedModule;if(!n)return;var b=n.style.maxWidth||'',a=controls.width.value;commit({target_type:'module',target:n.getAttribute('data-edit-module-id'),operation:'style_change',property:'max-width',before:b,after:a,authority:'HUMAN',scope:'HOW_OVERRIDE'});});
  controls.bg.addEventListener('change',function(){var n=state.selectedModule;if(!n)return;commit({target_type:'module',target:n.getAttribute('data-edit-module-id'),operation:'style_change',property:'background-color',before:n.style.backgroundColor||'',after:controls.bg.value,authority:'HUMAN',scope:'HOW_OVERRIDE'});});
  controls.border.addEventListener('change',function(){var n=state.selectedModule;if(!n)return;commit({target_type:'module',target:n.getAttribute('data-edit-module-id'),operation:'style_change',property:'border',before:n.style.border||'',after:controls.border.value,authority:'HUMAN',scope:'HOW_OVERRIDE'});});
  controls.layout.addEventListener('change',function(){
    var n=state.selectedModule;if(!n||controls.layout.value==='current')return;
    var b=n.getAttribute('style')||'';
    if(controls.layout.value==='single'){n.style.display='block';n.style.gridTemplateColumns='';n.style.flexDirection='';n.style.flexWrap='';}
    if(controls.layout.value==='two'){n.style.display='grid';n.style.gridTemplateColumns='repeat(2,minmax(0,1fr))';n.style.gap=n.style.gap||'16px';n.style.flexDirection='';}
    if(controls.layout.value==='row'){n.style.display='flex';n.style.flexDirection='row';n.style.flexWrap='wrap';n.style.gap=n.style.gap||'16px';n.style.gridTemplateColumns='';}
    if(controls.layout.value==='column'){n.style.display='flex';n.style.flexDirection='column';n.style.gap=n.style.gap||'16px';n.style.gridTemplateColumns='';}
    var a=n.getAttribute('style')||'';
    // Restore then commit so undo/redo owns the mutation.
    if(b) n.setAttribute('style',b); else n.removeAttribute('style');
    commit({target_type:'module',target:n.getAttribute('data-edit-module-id'),operation:'style_attr',before:b,after:a,authority:'HUMAN',scope:'HOW_OVERRIDE'});
  });

  function moveSelected(delta){
    var m=state.selectedModule;if(!m||m.getAttribute('data-edit-movable')!=='true')return;
    var before=currentModuleIndex(m), after=before+delta; if(before<0)return;
    var count=Array.prototype.filter.call(m.parentElement.children,function(x){return x.hasAttribute&&x.hasAttribute('data-edit-module-id');}).length;
    after=Math.max(0,Math.min(after,count-1)); if(after===before)return;
    commit({target_type:'module',target:m.getAttribute('data-edit-module-id'),operation:'move_module',before:before,after:after,authority:'HUMAN',scope:'NARRATIVE_ORDER_OVERRIDE'});
  }
  controls.moveUp.addEventListener('click',function(){moveSelected(-1);}); controls.moveDown.addEventListener('click',function(){moveSelected(1);});

  function resetElement(){
    var n=state.selectedElement;if(!n)return;var id=n.getAttribute('data-edit-id'),base=baseState.elements&&baseState.elements[id];if(!base)return;
    if(n.textContent!==base.text) commit({target_type:'element',target:id,operation:'text_replace',before:n.textContent,after:base.text,authority:'HUMAN',scope:'RESET'});
    var cur=n.getAttribute('style')||'', bs=base.style||''; if(cur!==bs) commit({target_type:'element',target:id,operation:'style_attr',before:cur,after:bs,authority:'HUMAN',scope:'RESET'});
  }
  function resetModule(){
    var m=state.selectedModule;if(!m)return;var mid=m.getAttribute('data-edit-module-id'),base=baseState.modules&&baseState.modules[mid];
    if(base){var cur=m.getAttribute('style')||'',bs=base.style||'';if(cur!==bs)commit({target_type:'module',target:mid,operation:'style_attr',before:cur,after:bs,authority:'HUMAN',scope:'RESET'}); if(m.getAttribute('data-edit-movable')==='true' && typeof base.index==='number' && currentModuleIndex(m)!==base.index)commit({target_type:'module',target:mid,operation:'move_module',before:currentModuleIndex(m),after:base.index,authority:'HUMAN',scope:'RESET'});}
    m.querySelectorAll('[data-edit-id]').forEach(function(n){var id=n.getAttribute('data-edit-id'),b=baseState.elements&&baseState.elements[id];if(!b)return;if(n.textContent!==b.text)commit({target_type:'element',target:id,operation:'text_replace',before:n.textContent,after:b.text,authority:'HUMAN',scope:'RESET'});var cs=n.getAttribute('style')||'',bs2=b.style||'';if(cs!==bs2)commit({target_type:'element',target:id,operation:'style_attr',before:cs,after:bs2,authority:'HUMAN',scope:'RESET'});});
  }
  function resetPage(){
    Object.keys(baseState.elements||{}).forEach(function(id){var n=doc.querySelector('[data-edit-id="'+cssEsc(id)+'"]'),b=baseState.elements[id];if(!n)return;if(n.textContent!==b.text)commit({target_type:'element',target:id,operation:'text_replace',before:n.textContent,after:b.text,authority:'HUMAN',scope:'RESET'});var cs=n.getAttribute('style')||'',bs=b.style||'';if(cs!==bs)commit({target_type:'element',target:id,operation:'style_attr',before:cs,after:bs,authority:'HUMAN',scope:'RESET'});});
    Object.keys(baseState.modules||{}).forEach(function(id){var n=doc.querySelector('[data-edit-module-id="'+cssEsc(id)+'"]'),b=baseState.modules[id];if(!n)return;var cs=n.getAttribute('style')||'',bs=b.style||'';if(cs!==bs)commit({target_type:'module',target:id,operation:'style_attr',before:cs,after:bs,authority:'HUMAN',scope:'RESET'});if(n.getAttribute('data-edit-movable')==='true'&&typeof b.index==='number'&&currentModuleIndex(n)!==b.index)commit({target_type:'module',target:id,operation:'move_module',before:currentModuleIndex(n),after:b.index,authority:'HUMAN',scope:'RESET'});});
  }
  resetElBtn.addEventListener('click',resetElement); resetModBtn.addEventListener('click',resetModule); resetPageBtn.addEventListener('click',function(){ if(window.confirm('恢复全部人工修改到 Generated Base？该动作本身也会进入撤销历史。')) resetPage(); });

  function sanitizeClone(clean){
    syncLedger();
    var clone=doc.documentElement.cloneNode(true);
    clone.classList.remove('he-editing');
    var cloneBody=clone.querySelector('body'); if(cloneBody) cloneBody.classList.remove('he-editing');
    clone.querySelectorAll('[data-he-runtime-ui]').forEach(function(n){n.remove();});
    clone.querySelectorAll('.he-selected-element,.he-selected-module').forEach(function(n){n.classList.remove('he-selected-element','he-selected-module');});
    clone.querySelectorAll('[contenteditable]').forEach(function(n){n.removeAttribute('contenteditable');});
    if(clean){
      ['he-editor-style','he-editor-script','human-edit-ledger','human-edit-base-state','human-edit-meta'].forEach(function(id){var n=clone.querySelector('#'+id);if(n)n.remove();});
      clone.querySelectorAll('[data-edit-id]').forEach(function(n){n.removeAttribute('data-edit-id');n.removeAttribute('data-edit-type');n.removeAttribute('data-edit-authority');n.removeAttribute('data-edit-obligation-refs');});
      clone.querySelectorAll('[data-edit-module-id]').forEach(function(n){n.removeAttribute('data-edit-module-id');n.removeAttribute('data-edit-movable');});
      clone.querySelectorAll('[data-motion-reveal]').forEach(function(n){n.removeAttribute('data-motion-reveal');});
      clone.querySelectorAll('[spellcheck]').forEach(function(n){n.removeAttribute('spellcheck');});
    } else {
      var ln=clone.querySelector('#human-edit-ledger'); if(ln) ln.textContent=JSON.stringify(ledger,null,2);
    }
    return '<!DOCTYPE html>\n'+clone.outerHTML;
  }

  function download(name, text, type){
    var blob=new Blob([text],{type:type||'text/plain;charset=utf-8'});var url=URL.createObjectURL(blob);var a=doc.createElement('a');a.href=url;a.download=name;doc.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(url);},1200);
  }
  function stamp(){var d=new Date();return d.getFullYear()+String(d.getMonth()+1).padStart(2,'0')+String(d.getDate()).padStart(2,'0')+'-'+String(d.getHours()).padStart(2,'0')+String(d.getMinutes()).padStart(2,'0');}
  exportEditableBtn.addEventListener('click',function(){download('report-edited-'+stamp()+'.html',sanitizeClone(false),'text/html;charset=utf-8');});
  exportCleanBtn.addEventListener('click',function(){download('report-published-'+stamp()+'.html',sanitizeClone(true),'text/html;charset=utf-8');});
  exportPatchBtn.addEventListener('click',function(){syncLedger();download('human-edit-history-'+stamp()+'.json',JSON.stringify(ledger,null,2),'application/json;charset=utf-8');});

  window.addEventListener('keydown',function(e){
    if(!state.editing)return;
    var active=doc.activeElement, typing=active && (active.isContentEditable || /INPUT|TEXTAREA|SELECT/.test(active.tagName));
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='z'&&!typing){e.preventDefault();if(e.shiftKey)redo();else undo();}
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='y'&&!typing){e.preventDefault();redo();}
    if(e.key==='Escape'&&!typing){setEditing(false);}
  });

  // Preserve existing report behavior; editor starts opt-in and local-only.
  setEditing(false);
  syncLedger();
})();
