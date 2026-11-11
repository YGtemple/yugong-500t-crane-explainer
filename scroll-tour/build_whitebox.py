# -*- coding: utf-8 -*-
import re
from pathlib import Path

base = Path(r"C:\Users\罗景祺\Doubao\chats\2026-11-10\new-chat-1\500t门机交互科普页")
main = (base / "500t门机交互科普页.html").read_text(encoding="utf-8")
tour_path = base / "scroll-tour" / "index.html"
tour = tour_path.read_text(encoding="utf-8")

def extract(html, sid):
    m = re.search(r'<script id="%s">(.*?)</script>' % re.escape(sid), html, re.S)
    if not m:
        raise RuntimeError("missing " + sid)
    return m.group(1)

three_js = extract(main, "three-lib-inline")
gltf_js = extract(main, "gltf-lib-inline")
glb_js = extract(main, "white-crane-glb")
for nm in ("three_js", "gltf_js", "glb_js"):
    locals()[nm] = locals()[nm].replace("</script>", "<\\/script>")

# ---------- CSS ----------
wb_css = """
    /* ===== 白模运镜预演弹层 ===== */
    .in-modal__card--wb{width:min(760px,100%)}
    .wb-stage{position:relative;margin:0 28px;height:380px;border-radius:14px;overflow:hidden;background:#0f1824}
    #wbCanvas{width:100%;height:100%;display:block}
    .wb-state{position:absolute;top:12px;left:12px;background:rgba(15,24,36,.72);color:#cfe0f5;font-size:12px;font-weight:600;padding:6px 12px;border-radius:999px;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
    .wb-controls{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:16px 28px 26px}
    .wb-btn{background:#d23b30;color:#fff;font-weight:700;font-size:13px;padding:9px 18px;border-radius:999px}
    .wb-btn:hover{background:#b8312a}
    .wb-note{font-size:11.5px;color:#76869c;flex:1;min-width:160px;line-height:1.6}
    .wb-open-btn{display:block;width:100%;margin-top:16px;background:#16202e;color:#fff;font-weight:700;font-size:13.5px;padding:12px;border-radius:10px}
    .wb-open-btn:hover{background:#d23b30}
    @media (max-width:600px){
      .wb-stage{margin:0 18px;height:280px}
      .wb-controls{padding:14px 20px 22px}
    }
"""

# ---------- 弹层 HTML ----------
wb_html = """
  <!-- 白模运镜预演弹层（不跳页） -->
  <div class="in-modal" id="wbModal" hidden>
    <div class="in-modal__card in-modal__card--wb">
      <button class="in-modal__close" id="wbModalClose" type="button" aria-label="关闭">&times;</button>
      <div class="in-modal__head">
        <span class="in-modal__kicker">WHITEBOX PREVIS</span>
        <h3>白模运镜预演</h3>
        <p>正式生成前，先用预制白模确定机位与运镜（previs），再据此生成写实成片。</p>
      </div>
      <div class="wb-stage">
        <canvas id="wbCanvas"></canvas>
        <div class="wb-state" id="wbState">白模加载中…</div>
      </div>
      <div class="wb-controls">
        <button id="wbReplay" class="wb-btn" type="button">重新预演</button>
        <span class="wb-note">白模为团队按白膜图参数化建模（桁架式结构示意），尺寸为推定值，仅作运镜预演。</span>
      </div>
    </div>
  </div>
"""

# 参数弹层加入口按钮（在 .in-back 前）
anchor_back = '<a class="in-back" href="../500t门机交互科普页.html">'
assert anchor_back in tour
entry_btn = '<button class="wb-open-btn" id="btnOpenWb" type="button">查看白模运镜预演</button>\n        '
tour = tour.replace(anchor_back, entry_btn + anchor_back, 1)

# 注入 CSS（在最后一个 </style> 前）
tour = tour.replace("  </style>", wb_css + "\n  </style>", 1)

# 注入弹层 HTML（在第一个 <script src="scrub-engine.js"> 前）
anchor_scrub = '  <script src="scrub-engine.js"></script>'
assert anchor_scrub in tour
tour = tour.replace(anchor_scrub, wb_html + "\n" + anchor_scrub, 1)

tour_path.write_text(tour, encoding="utf-8")
print("stage1 ok")
