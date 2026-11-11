# -*- coding: utf-8 -*-
"""
在 Blender 里参数化建一台 500t 双主梁门式起重机白模，导出给网页导演台/手机取景实时用。
单位：米；沿 X 轴为轨道方向，Y 向上。
运行：
  blender.exe -b -P build_director_crane.py -- <out.glb>
"""
import bpy, sys, math, os

argv = sys.argv
out_glb = argv[argv.index('--') + 1] if '--' in argv else 'director_crane.glb'

# ---------- 清场 ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------- 材质 ----------
def mat(name, rgb, rough=0.86, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metal
    return m

WHITE = mat('白模-结构', (0.86, 0.88, 0.91), 0.92)
GREY  = mat('白模-附件', (0.66, 0.70, 0.75), 0.85, 0.15)
DARK  = mat('白模-行走', (0.42, 0.46, 0.52), 0.80, 0.25)

PARTS = []

def box(name, sx, sy, sz, x, y, z, m=WHITE, rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    o = bpy.context.active_object
    o.name = name
    o.scale = (sx, sy, sz)
    if rot:
        o.rotation_euler = rot
    o.data.materials.append(m)
    PARTS.append(o)
    return o

def cyl(name, r, h, x, y, z, m=DARK, rot=None, seg=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r, depth=h, location=(x, y, z))
    o = bpy.context.active_object
    o.name = name
    if rot:
        o.rotation_euler = rot
    o.data.materials.append(m)
    PARTS.append(o)
    return o

# ---------- 参数（500t 门机，示意尺寸） ----------
SPAN   = 40.0   # 轨距 / 跨度
HEIGHT = 30.0   # 主梁下沿高度
DEPTH  = 12.0   # 门架前后腿间距
LEG    = 1.5    # 支腿截面
RAIL_L = 56.0   # 轨道长度（要落在导演台 60×40 的场景盒内）

# ---------- 轨道与台车 ----------
for z in (-DEPTH / 2, DEPTH / 2):
    box('轨道', RAIL_L, 0.32, 0.9, 0, 0.16, z, DARK)

for x in (-SPAN / 2, SPAN / 2):
    for z in (-DEPTH / 2, DEPTH / 2):
        box('台车', 4.2, 1.1, 2.8, x, 0.9, z, GREY)
        for dz in (-0.9, 0.9):
            cyl('车轮', 0.45, 0.4, x, 0.45, z + dz, DARK, rot=(0, math.pi / 2, 0), seg=10)
            cyl('车轮', 0.45, 0.4, x, 0.45, z + dz, DARK, rot=(0, math.pi / 2, 0), seg=10)

# ---------- 四条支腿 ----------
for x in (-SPAN / 2, SPAN / 2):
    for z in (-DEPTH / 2, DEPTH / 2):
        box('支腿', LEG, HEIGHT, LEG, x, HEIGHT / 2 + 1.2, z, WHITE)

# 下横梁（两端，沿 Z 连接前后腿）
for x in (-SPAN / 2, SPAN / 2):
    box('下横梁', 1.1, 1.2, DEPTH + LEG, x, 7.0, 0, WHITE)
    box('上横梁', 1.0, 1.1, DEPTH + LEG, x, HEIGHT - 2.2, 0, WHITE)

# 端部斜撑（Y-Z 平面）
for x in (-SPAN / 2, SPAN / 2):
    for sgn in (-1, 1):
        dy, dz = HEIGHT - 9.0, DEPTH * 0.55
        L = math.hypot(dy, dz)
        ang = math.atan2(dz, dy) * sgn
        box('斜撑', 0.34, L, 0.34, x, 8.6 + dy / 2, sgn * DEPTH * 0.28, WHITE, rot=(ang, 0, 0))

# 主梁（双主梁）
GIRDER_Y = HEIGHT + 1.1
for z in (-2.7, 2.7):
    box('主梁', SPAN + 4.6, 2.2, 1.9, 0, GIRDER_Y, z, WHITE)
    # 主梁腹板加劲（走台栏杆示意）
    box('走台', SPAN + 4.0, 0.14, 0.9, 0, GIRDER_Y + 1.2, z + (1.85 if z > 0 else -1.85), GREY)

# 端梁（连两主梁）
for x in (-(SPAN + 4.6) / 2 + 0.6, (SPAN + 4.6) / 2 - 0.6):
    box('端梁', 1.3, 2.0, 7.6, x, GIRDER_Y, 0, WHITE)

# ---------- 小车 ----------
TROLLEY_Y = GIRDER_Y + 2.3
box('小车', 6.0, 2.2, 5.4, 0, TROLLEY_Y, 0, GREY)
box('小车机房', 4.4, 1.9, 4.0, 0, TROLLEY_Y + 2.0, 0, WHITE)
for dz in (-1.6, 1.6):
    box('小车端梁', 2.4, 1.0, 1.2, 0, TROLLEY_Y - 1.4, dz, GREY)

# ---------- 起升绳 + 吊具 ----------
HOOK_Y = 12.5
for dx in (-0.9, 0.9):
    for dz in (-0.9, 0.9):
        cyl('起升绳', 0.09, TROLLEY_Y - 1.0 - HOOK_Y, dx, (TROLLEY_Y - 1.0 + HOOK_Y) / 2, dz, DARK, seg=6)
box('吊具横梁', 5.2, 0.8, 1.2, 0, HOOK_Y + 0.6, 0, GREY)
box('吊钩组', 2.0, 1.6, 1.6, 0, HOOK_Y - 0.6, 0, DARK)

# ---------- 司机室 ----------
CAB_X, CAB_Z = SPAN / 2 - 4.0, DEPTH / 2 + 2.2
box('司机室托架', 3.0, 0.5, 3.0, CAB_X, 20.0, CAB_Z - 1.2, GREY)
box('司机室', 3.2, 2.9, 3.0, CAB_X, 21.7, CAB_Z - 0.2, WHITE)
box('司机室顶', 3.6, 0.25, 3.4, CAB_X, 23.3, CAB_Z - 0.2, GREY)

# ---------- 爬梯 ----------
for z in (-DEPTH / 2 + 0.9, DEPTH / 2 - 0.9):
    box('爬梯', 0.12, HEIGHT - 3.0, 0.9, SPAN / 2 - 1.6, (HEIGHT - 3.0) / 2 + 1.2, z, GREY)
    for k in range(9):
        box('爬梯横档', 0.6, 0.07, 0.9, SPAN / 2 - 1.6, 3.5 + k * 2.6, z, GREY)

# ---------- 合并导出 ----------
for o in PARTS:
    o.select_set(True)
bpy.context.view_layer.objects.active = PARTS[0]

os.makedirs(os.path.dirname(out_glb), exist_ok=True) if os.path.dirname(out_glb) else None
bpy.ops.export_scene.gltf(
    filepath=out_glb,
    export_format='GLB',
    export_apply=True,
    export_yup=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False,
)

stats = {
    'objects': len(PARTS),
    'triangles': sum(len(o.data.loop_triangles) if o.data.loop_triangles else 0 for o in PARTS),
    'bytes': os.path.getsize(out_glb),
    'bbox': None,
}
bpy.context.view_layer.update()
xs = []
for o in PARTS:
    for v in o.bound_box:
        pass
print('BUILD_OK', stats, flush=True)
