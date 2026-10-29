# Anatomical hands for the AuraWake gesture drawings (owner, 2026-10-29: "le mani così sono proprio brutte").
# MPFB2 (MakeHuman for Blender, CC0 base mesh) makes a human with its default rig; the fingers are posed, the right
# hand and forearm are cut out and written as OBJ in the frame aura.py uses for hands: wrist at the origin, X along
# the fingers, Y towards the thumb, Z the back of the hand (metres). Tips of thumb and index go to hands.json.
#   blender -b -P deck/blender/hand_mpfb.py
import bpy, json, math, os
from mathutils import Vector, Matrix
from bl_ext.user_default.mpfb.services.humanservice import HumanService

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hands')
os.makedirs(OUT, exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)

body = HumanService.create_human(scale=0.1)
rig = HumanService.add_builtin_rig(body, 'default')
bpy.context.view_layer.update()
PB = rig.pose.bones
for pb in PB: pb.rotation_mode = 'XYZ'
W = rig.matrix_world
def head(n): return W @ PB[n].head
def tail(n): return W @ PB[n].tail
def upd(): bpy.context.view_layer.update()

def frame():
    """Hand frame from the posed bones: origin at the wrist, X to the middle knuckle, Y across to the index side."""
    o = head('wrist.R'); x = (head('finger3-1.R') - o).normalized()
    y = head('finger2-1.R') - head('finger5-1.R'); y = (y - x * x.dot(y)).normalized()
    return o, Matrix((x, y, x.cross(y))).transposed()

O0, R0 = frame(); PALM = -(R0.col[2])                # palm side, in world space

def flex_axis(name):
    """Local axis and sign that curl this bone's tip towards the palm."""
    pb = PB[name]; t0 = tail(name); best = None
    for ax in (0, 2):
        for sg in (1, -1):
            pb.rotation_euler = (0, 0, 0); pb.rotation_euler[ax] = sg * 0.4; upd()
            d = (tail(name) - t0).dot(PALM)
            if best is None or d > best[0]: best = (d, ax, sg)
    pb.rotation_euler = (0, 0, 0); upd()
    return best[1], best[2]

FING = {'index': 2, 'middle': 3, 'ring': 4, 'little': 5}
AX = {f'finger{i}-{j}.R': flex_axis(f'finger{i}-{j}.R') for i in range(1, 6) for j in (1, 2, 3)}

def curl(pose):
    for k, i in FING.items():
        for j, a in enumerate(pose[k], 1):
            n = f'finger{i}-{j}.R'; ax, sg = AX[n]; e = [0, 0, 0]; e[ax] = sg * math.radians(a); PB[n].rotation_euler = e
    upd()

def local(p):
    o, R = frame(); return R.transposed() @ (p - o)

def solve_thumb(target):
    """Coordinate descent on the thumb's three joints (two axes at its root) so its tip lands on target (hand frame)."""
    names = ['finger1-1.R', 'finger1-1.R', 'finger1-2.R', 'finger1-3.R']; axes = [0, 2, AX['finger1-2.R'][0], AX['finger1-3.R'][0]]
    ang = [0.0] * 4
    def cost():
        for n in set(names): PB[n].rotation_euler = (0, 0, 0)
        for n, ax, a in zip(names, axes, ang): PB[n].rotation_euler[ax] += a
        upd(); return (local(tail('finger1-3.R')) - target).length
    c = cost(); step = 0.35
    while step > 0.004:
        moved = False
        for i in range(4):
            for d in (step, -step):
                ang[i] += d; c2 = cost()
                if c2 < c - 1e-6: c = c2; moved = True; break
                ang[i] -= d
        if not moved: step /= 2
    cost(); return c

POSES = {
    'palm': {'index': (6, 34, 18), 'middle': (5, 38, 20), 'ring': (6, 36, 18), 'little': (8, 30, 14)},
    'pinch': {'index': (35, 65, 35), 'middle': (65, 75, 40), 'ring': (70, 80, 40), 'little': (75, 80, 40)},
}
KEEP = {'wrist.R', 'lowerarm01.R', 'lowerarm02.R', 'upperarm02.R'}   # past the elbow: the arm always leaves the frame
KEEP = KEEP | {f'metacarpal{i}.R' for i in range(1, 5)} | set(AX)
def straighten_elbow():
    """The rest pose bends the elbow; line the forearm up with the upper arm so the arm runs straight off the frame."""
    la = PB['lowerarm01.R']; h = la.head.copy()
    up = (PB['upperarm02.R'].tail - PB['upperarm02.R'].head).normalized()
    lo = (PB['lowerarm02.R'].tail - la.head).normalized()
    q = lo.rotation_difference(up).to_matrix().to_4x4()
    la.matrix = Matrix.Translation(h) @ q @ Matrix.Translation(-h) @ la.matrix; upd()

info = {}
for name, pose in POSES.items():
    for pb in PB: pb.rotation_euler = (0, 0, 0)
    upd(); straighten_elbow()
    curl(pose)
    if name == 'pinch':          # thumb pad opposite the index pad, across the band (gap as in the procedural hand)
        it = local(tail('finger2-3.R'))
        err = solve_thumb(it + Vector((-0.0205, 0.0067, -0.008)))
        print(f'pinch: thumb error {err * 1000:.1f} mm')
    o, R = frame(); Rt = R.transposed()
    dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, depsgraph=dg)
    # the mask modifier drops the helpers, so evaluated indices differ from the base mesh: cut by geometry instead,
    # keeping every vertex whose nearest bone belongs to the hand or the forearm
    segs = [(pb.name, W @ pb.head, W @ pb.tail) for pb in PB]
    def near(p):
        best = (9.0, '')
        for n, h, t in segs:
            d = t - h; L2 = d.length_squared; u = 0.0 if L2 == 0 else max(0.0, min(1.0, (p - h).dot(d) / L2))
            dd = (p - (h + d * u)).length
            if dd < best[0]: best = (dd, n)
        return best[1]
    keep = {v.index for v in me.vertices if near(body.matrix_world @ v.co) in KEEP}
    lines = []; idx = {}
    for i in sorted(keep):
        p = Rt @ (body.matrix_world @ me.vertices[i].co - o); idx[i] = len(idx) + 1
        lines.append(f'v {p.x:.6f} {p.y:.6f} {p.z:.6f}')
    for f in me.polygons:
        if all(i in idx for i in f.vertices): lines.append('f ' + ' '.join(str(idx[i]) for i in f.vertices))
    open(os.path.join(OUT, f'{name}.obj'), 'w').write('\n'.join(lines) + '\n')
    info[name] = {'index': list(local(tail('finger2-3.R'))), 'thumb': list(local(tail('finger1-3.R'))),
                  'length': (head('finger3-1.R') - o).length}
    print(name, len(idx), 'verts')
json.dump(info, open(os.path.join(OUT, 'hands.json'), 'w'), indent=1)
