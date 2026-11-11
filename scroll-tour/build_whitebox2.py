# -*- coding: utf-8 -*-
import re
from pathlib import Path

base = Path(r"C:\Users\罗景祺\Doubao\chats\2026-11-10\new-chat-1\500t门机交互科普页")
main = (base / "500t门机交互科普页.html").read_text(encoding="utf-8")
tour_path = base / "scroll-tour" / "index.html"
tour = tour_path.read_text(encoding="utf-8")

def extract_block(html, sid):
    m = re.search(r'(<script id="%s">.*?</script>)' % re.escape(sid), html, re.S)
    if not m:
        raise RuntimeError("missing " + sid)
    return m.group(1).replace("</script>", "<\\/script>").replace(
        '<script id="%s">' % sid, "<script>", 1)

lib_three = extract_block(main, "three-lib-inline")
lib_gltf = extract_block(main, "gltf-lib-inline")
lib_glb = extract_block(main, "white-crane-glb")

previs = r"""<script>
(function(){
  var modal=document.getElementById('wbModal');
  var canvas=document.getElementById('wbCanvas');
  var stateEl=document.getElementById('wbState');
  var closeBtn=document.getElementById('wbModalClose');
  var replayBtn=document.getElementById('wbReplay');
  var openEntry=document.getElementById('btnOpenWb');
  var renderer,scene,camera,rafId;
  var inited=false,running=false;
  var frames=[],cur=0,frameT0=0;
  var FRAME_DUR=3200;
  var labels=['整机远景','门架正面','支腿与台车','主梁俯视','高位环绕','另一侧远景','拉远回整机'];

  function init(){
    renderer=new THREE.WebGLRenderer({canvas:canvas,antialias:true});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
    scene=new THREE.Scene();
    scene.background=new THREE.Color(0x0f1824);
    camera=new THREE.PerspectiveCamera(45,1,0.1,3000);
    scene.add(new THREE.HemisphereLight(0xffffff,0x304055,1.2));
    var dir=new THREE.DirectionalLight(0xffffff,0.9);
    dir.position.set(40,60,30);scene.add(dir);
    var b64=window.WHITE_CRANE_GLB_B64;
    var bin=atob(b64),buf=new Uint8Array(bin.length);
    for(var i=0;i<bin.length;i++)buf[i]=bin.charCodeAt(i);
    new THREE.GLTFLoader().parse(buf.buffer,'',function(gltf){
      var modelRoot=new THREE.Group();
      var inner=gltf.scene;
      inner.traverse(function(o){
        if(o.isMesh){
          if(o.name && o.name.indexOf('地面')>=0){o.visible=false;return;}
          o.castShadow=true;o.receiveShadow=true;
          (Array.isArray(o.material)?o.material:[o.material]).forEach(function(m){
            if(m){m.side=THREE.DoubleSide;if(m.color)m.color.setHex(0xd3dbe4);m.roughness=.85;m.metalness=.05;}
          });
        }
      });
      modelRoot.add(inner);
      var bb=new THREE.Box3().setFromObject(modelRoot);
      var cc=bb.getCenter(new THREE.Vector3());
      inner.position.set(-cc.x,-bb.min.y,-cc.z);
      scene.add(modelRoot);
      bb=new THREE.Box3().setFromObject(modelRoot);
      var size=bb.getSize(new THREE.Vector3());
      var h=size.y,half=Math.max(size.x,size.z)/2;
      var grid=new THREE.GridHelper(half*4,40,0x3a5170,0x24364e);
      scene.add(grid);
      function key(angle,dist,yp,ty){
        return{pos:new THREE.Vector3(Math.cos(angle)*dist,yp,Math.sin(angle)*dist),
               tar:new THREE.Vector3(0,ty||h*0.45,0)};
      }
      var D=half*1.45,Dn=half*0.85;
      frames=[key(0.6,D,h*.95),key(1.35,D,h*.8),key(2.1,Dn,h*.35,h*.2),
              key(2.9,D,h*1.35,h*.55),key(3.7,D,h*1.1),key(4.5,D,h*.85),
              key(5.4,D*1.2,h*.95)];
      camera.position.copy(frames[0].pos);camera.lookAt(frames[0].tar);
      inited=true;resize();
      stateEl.textContent='白模预演 · 整机远景';
      cur=0;frameT0=performance.now();running=true;loop();
    },function(){stateEl.textContent='白模加载失败';});
  }
  function resize(){
    var w=canvas.clientWidth||canvas.parentElement.clientWidth;
    var hh=canvas.clientHeight||canvas.parentElement.clientHeight;
    if(w&&hh&&renderer){renderer.setSize(w,hh,false);camera.aspect=w/hh;camera.updateProjectionMatrix();}
  }
  function loop(){
    rafId=requestAnimationFrame(loop);
    var now=performance.now();
    var k=Math.min((now-frameT0)/FRAME_DUR,1);
    var a=frames[cur],b=frames[(cur+1)%frames.length];
    var e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
    camera.position.lerpVectors(a.pos,b.pos,e);
    camera.lookAt(a.tar.clone().lerp(b.tar,e));
    stateEl.textContent='白模预演 · '+labels[cur];
    if(k>=1){cur=(cur+1)%frames.length;frameT0=now;}
    renderer.render(scene,camera);
  }
  function open(){
    modal.hidden=false;
    if(!inited){stateEl.textContent='白模加载中…';init();}
    else{resize();if(!running){running=true;frameT0=performance.now();loop();}}
    setTimeout(resize,60);setTimeout(resize,200);
  }
  function close(){
    modal.hidden=true;
    if(running){cancelAnimationFrame(rafId);running=false;}
  }
  closeBtn.addEventListener('click',close);
  modal.addEventListener('click',function(e){if(e.target===modal)close();});
  replayBtn.addEventListener('click',function(){cur=0;frameT0=performance.now();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!modal.hidden)close();});
  if(openEntry)openEntry.addEventListener('click',function(){
    document.getElementById('inModal').hidden=true;open();
  });
  window.addEventListener('resize',function(){if(!modal.hidden)resize();});
  window.__openWhitebox=open;
})();
</script>"""

inject = "\n  " + lib_three + "\n  " + lib_gltf + "\n  " + lib_glb + "\n  " + previs + "\n</body>"
tour = tour.replace("\n</body>", inject, 1)
tour_path.write_text(tour, encoding="utf-8")
print("stage2 ok")
