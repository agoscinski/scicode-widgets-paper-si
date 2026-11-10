"""Publication geometry only; notebook content is supplied by generate_figures.py."""

LAYOUT = r'''({i,w,h,overlay}) => {
 const roots=[...document.querySelectorAll('.jupyter-widgets.jp-OutputArea-output.jp-OutputArea-executeResult')]
    .map(e=>e.querySelector('.widget-subarea > .widget-vbox'));
 const stage=document.createElement('div');stage.id='composite';
 stage.style.cssText=`position:relative;width:${w}px;height:${h}px;background:white;overflow:hidden`;
 document.body.appendChild(stage);
 function place(e,x,y,width,scale=3,height=null){
   if(!e)throw Error('Missing widget element');
   stage.appendChild(e);e.style.cssText+=`;position:absolute!important;left:${x}px;top:${y}px;width:${width/scale}px;margin:0!important;padding:0!important;transform:scale(${scale});transform-origin:top left;`;
   if(height)e.style.height=height/scale+'px';
   return e;
 }
 function code(root,x,y,width,scale=3){
   const e=root.querySelector('.widget-code-input-signature').parentElement;
   place(e,x,y,width,scale);e.classList.add('publication-editor');return e;
 }
 function button(root,label,x,y,width,height,scale=3){
   const e=[...root.querySelectorAll('button')].find(e=>e.textContent.trim()==label);
   place(e,x,y,width,scale,height);return e;
 }
 if(i===1){
   code(roots[0],50,1830,1232);
   place(roots[0].querySelector('.widget-slider'),40,2156,1110,3);
   button(roots[0],'Run Code',48,2262,556,128);
   const plot=place(roots[0].querySelector('[data-mime-type="image/png"]'),52,2430,1235,3);
   plot.querySelector('img').style.setProperty('width','411.666667px','important');
   stage.classList.add('figure-one');
 }
 if(i===2){
   code(roots[0],39,2070,1540,3.04);
   button(roots[0],'Check Code',30,2306,460,100,3.04);
   const output=roots[0].querySelector('[data-mime-type="application/vnd.jupyter.stdout"] pre');
   const chunks=output.innerHTML.trim().split(/\n\n+/);
   chunks.slice(0,3).forEach((chunk,k)=>{
     const pre=document.createElement('pre');pre.innerHTML=chunk;
     place(pre,55,[2440,3068,3280][k],1540,3.04);
     pre.style.setProperty('line-height','16.8px','important');
   });
 }
 if(i===3){
   if(roots.length!==4)throw Error('Figure 3 needs four executed snapshots');
   stage.classList.add('figure-three');
   const panels=[{x:275,y:0,w:548,h:234,s:1.5}, {x:0,y:297,w:530,h:463,s:1.5},
                 {x:587,y:292,w:447,h:234,s:1.25},{x:587,y:548,w:447,h:234,s:1.25}];
   panels.forEach((p,k)=>{
     const border=document.createElement('div');border.style.cssText=`position:absolute;left:${p.x}px;top:${p.y}px;width:${p.w}px;height:${p.h}px;border:1px solid #9d9d9d;box-sizing:border-box`;stage.appendChild(border);
     const r=roots[k],s=p.s;
     code(r,p.x+22,p.y+2,p.w-23,s);
     place(r.querySelector('.widget-slider'),p.x+16,p.y+106*s/1.5,p.w-35,s);
     const check=button(r,'Check Code',p.x+10,p.y+158*s/1.5,(p.w-34)/2,56*s/1.5,s);
     const run=button(r,'Run Code',p.x+18+(p.w-34)/2,p.y+158*s/1.5,(p.w-34)/2,56*s/1.5,s);
     check.style.setProperty('background-color',k===1?'#f4f2f0':'#56b2e4','important');
     run.style.setProperty('background-color',k===2?'#f4f2f0':'#d85e33','important');
     [check,run].forEach(e=>e.style.setProperty('font-size',(k<2?23/s:17/s)+'px','important'));
     const logs=[...r.querySelectorAll('[data-mime-type="application/vnd.jupyter.stdout"]')];
     logs.forEach(e=>{
       place(e,p.x+20,p.y+(k===1?238:203),p.w-36,s);
       // Reparenting must retain the stale-output cue inherited in the notebook.
       if(k===3)e.style.opacity='0.4';
     });
     function cue(x,y,width,height,color){const e=document.createElement('div');e.style.cssText=`position:absolute;left:${x}px;top:${y}px;width:${width}px;height:${height}px;background:${color}`;stage.appendChild(e)}
     if(k===0){cue(281,5,8,151,'#d85e33');cue(290,5,8,94,'#56b2e4')}
     if(k===1)cue(12,306,8,141,'#d85e33');
     if(k===2)cue(597,297,7,83,'#56b2e4');
     if(k===3){cue(598,553,6,77,'#56b2e4');cue(592,630,5,46,'#d85e33')}
   });
 }
 stage.insertAdjacentHTML('beforeend',overlay);
 for(const child of [...document.body.children])if(child!==stage&&child.tagName!=='SCRIPT')child.style.display='none';
}'''

STYLE = r'''
#composite .cm-editor {font:13.333333px/18.333333px Menlo,monospace!important}
#composite .cm-scroller {font:13.333333px/18.333333px Menlo,monospace!important}
#composite .cm-content {padding:5px 0!important;min-height:0!important}
#composite .widget-code-input-signature {height:27px!important;overflow:hidden!important}
#composite .widget-code-input-body {height:40px!important;overflow:hidden!important}
#composite .cm-cursor {display:none!important}
#composite button {font:13px Arial,sans-serif!important;border-radius:2px!important}
#composite .widget-label {font:13px Arial,sans-serif!important}
#composite pre {font:13.333333px/17.5px Menlo,monospace!important;margin:0!important;white-space:pre-wrap!important}
#composite img {max-width:none!important}
#composite.figure-one .widget-code-input-signature {height:38.666667px!important}
#composite.figure-one .widget-code-input-body {height:61.333333px!important}
#composite.figure-one .cm-editor, #composite.figure-one .cm-scroller {font-size:16px!important;line-height:23.333333px!important}
#composite.figure-one .widget-code-input-signature .cm-content {padding:9px 0!important}
#composite.figure-one .widget-code-input-body .cm-content {padding:12px 0!important}
#composite.figure-three .widget-code-input-signature {height:35.333333px!important}
#composite.figure-three .widget-code-input-signature .cm-content {padding:10px 0!important}
#composite.figure-three .widget-code-input-body {height:30px!important}
#composite .ansi-bold {font-weight:bold!important}
#composite .ansi-red-intense-fg {color:#a43736!important}
#composite .ansi-green-intense-fg {color:#317231!important}
#composite .ansi-blue-intense-fg {color:#2a63c3!important}
'''
CLEAN = r'''
.jp-InputArea, .jp-OutputPrompt, .jp-InputPrompt,
.jp-OutputArea-output[data-mime-type="application/vnd.jupyter.stderr"] {display:none!important}
body, main {margin:0!important; padding:0!important; background:white!important}
.jp-Notebook {padding:0!important}
.jp-Cell {padding:0!important; margin:0!important}
.jp-OutputArea-child {padding:0!important; margin:0!important}
.jp-OutputArea-output {padding:0!important; margin:0!important}
.widget-subarea {padding:0!important}
'''

LAYOUT4 = r'''() => {
 const outputs = [...document.querySelectorAll('.jupyter-widgets.jp-OutputArea-output.jp-OutputArea-executeResult')];
 const roots = outputs.map(e => e.querySelector('.widget-subarea > .widget-vbox'));
 const stage = document.createElement('div'); stage.id='publication';
 stage.style.cssText='position:relative;width:535.333333px;height:1169.333333px;background:white;overflow:hidden';
 document.body.appendChild(stage);
 function place(e,x,y,w,h) {
   if(!e) throw Error('Missing widget element');
   stage.appendChild(e); e.style.cssText += `;position:absolute!important;left:${x}px;top:${y}px;width:${w}px;${h ? 'height:'+h+'px;' : ''}margin:0!important;padding:0!important;`;
 }
 // Keep text exercises in normal flow: display math includes limits below
 // the baseline, so a fixed textarea top can overlap the arg-min subscript.
 function textAnswer(root,y,width,height) {
   const flow=document.createElement('div');
   place(flow,10,y,510);
   flow.style.display='flex';
   flow.style.flexDirection='column';
   flow.style.gap='8px';
   const description=root.querySelector('.exercise-description');
   const textarea=root.querySelector('.widget-textarea');
   description.style.cssText+=';width:510px;margin:0!important;padding:0!important;flex:none;';
   textarea.style.cssText+=`;width:${width}px;height:${height}px;margin:0!important;padding:0!important;flex:none;`;
   flow.append(description,textarea);
 }
 place(roots[0].querySelector('.exercise-title'),10,5,520);
 textAnswer(roots[0],35,418,49);
 place(roots[1].querySelector('.exercise-title'),9,225,520);
 place(roots[1].querySelector('.exercise-description'),10,268,510);
 place(roots[1].querySelector('.widget-code-input-signature').parentElement,12,384,524);
 const sliders=[...roots[1].querySelectorAll('.widget-slider')];
 sliders.forEach((e,i)=>place(e,10,480+i*32,305,28));
 place(roots[1].querySelector('button'),9,605,153.33,41.67);
 place(roots[1].querySelector('[data-mime-type="application/vnd.jupyter.stdout"]'),17,656,510);
 place(roots[1].querySelector('[data-mime-type="image/png"]'),4,679.7,470);
 place(roots[2].querySelector('.exercise-title'),10,1038,520);
 textAnswer(roots[2],1068,457,48);
 for(const child of [...document.body.children]) if(child!==stage && child.tagName!=='SCRIPT') child.style.display='none';
}'''

STYLE4 = r'''
#publication .exercise-title {font: bold 20px Helvetica,Arial,sans-serif!important;overflow:visible}
#publication .exercise-title:first-child {font-size:18px!important}
#publication .exercise-description {font:13.333333px/19px Verdana,Arial,sans-serif!important;word-spacing:normal!important;overflow:visible}
#publication p {margin:0!important;width:500px!important}
#publication .widget-html-content, #publication .widget-htmlmath-content {padding:0!important;margin:0!important}
#publication .cm-editor {font:13.333333px/18.33px Menlo,monospace!important}
#publication .cm-scroller {font-family:Menlo,monospace!important;line-height:18.33px!important}
#publication .cm-content {padding:5px 0!important;min-height:0!important}
#publication .widget-code-input-signature {height:27px!important;overflow:hidden!important}
#publication .widget-code-input-body {height:66px!important;overflow:hidden!important}
#publication .widget-slider {font-size:13px!important}
#publication .widget-label {width:87px!important;min-width:87px!important}
#publication .widget-slider .slider-container {width:130px!important;flex:0 0 130px!important}
#publication button {font:13px Verdana,sans-serif!important;border-radius:3px}
#publication pre {font:13.333333px Menlo,monospace!important;line-height:18px!important;margin:0!important}
#publication img {width:460px!important;max-width:none!important}
'''


SOURCE_PANELS = {
    1: [(0, 2, 40, 12, 1245, 230, 44.8),
        (3, 3, 40, 269, 1245, 177, 44.9),
        (4, 4, 40, 478, 1245, 64, 44.9),
        (5, 5, 37, 585, 1245, 64, 44.9),
        (6, 6, 39, 696, 1245, 415, 44.9),
        (7, 7, 38, 1168, 1245, 373, 44.9)],
    2: [(3, 4, 20, 12, 1550, 367, 40.6),
        (5, 5, 20, 408, 1550, 514, 40.6),
        (6, 7, 20, 985, 1550, 575, 40.6),
        (8, 8, 20, 1641, 1550, 345, 40.6)],
}

SETUP = """%matplotlib inline
from IPython.display import display
import matplotlib as mpl
# scwidgets 0.2.3 expects the canonical pre-3.10 inline backend name.
mpl.backends.backend = 'module://matplotlib_inline.backend_inline'
mpl.rcParams['figure.dpi'] = 100
"""

# These select the paper's interactive state; they do not change notebook text.
CAPTURE_STATE = {
    1: """code_ex.parameters_panel.update_parameters({'frequency': 1.6})
figure.set_size_inches(4.5, 2.5)
code_ex.run_update()
figure.gca().set_xlim(-5.5, 5.5)
figure.gca().set_ylim(-1.1, 1.1)
figure.gca().set_yticks([-1, -0.5, 0, 0.5, 1])
code_ex._cue_outputs[0].clear_output(wait=True)
code_ex._cue_outputs[0].draw_display()
""",
    2: 'code_ex.run_check()',
    4: """code_input.docstring = ''
parameter_panel.update_parameters({'regularizer_log10': 0})
code_ex.run_update()
""",
}
FIGURE3_STATES = ['', 'code_ex.run_check()', 'code_ex.run_update()',
                  "code_ex.run_update()\ncode_ex.parameters_panel.update_parameters({'x': 8})"]


ADD_SOURCE = r'''panels => {
 const stage=document.querySelector('#composite');
 for(const p of panels){
   const box=document.createElement('div');box.className='notebook-source';
   box.style.cssText=`position:absolute;left:${p.x}px;top:${p.y}px;width:${p.w}px;height:${p.h}px;z-index:19`;
   const pre=document.createElement('pre');pre.innerHTML=p.html;
   pre.style.cssText=`font:${p.font}px/1.36 Menlo,monospace!important;white-space:pre-wrap!important;overflow-wrap:anywhere;margin:0!important`;
   box.appendChild(pre);stage.appendChild(box);
   // Fit complete source statements without truncating comments or text.
   let size=p.font;
   while((pre.scrollHeight>p.h || pre.scrollWidth>p.w) && size>8){
     size-=0.25;pre.style.setProperty('font-size',size+'px','important');
   }
   if(pre.scrollHeight>p.h || pre.scrollWidth>p.w)throw Error('Source panel does not fit');
 }
}'''

