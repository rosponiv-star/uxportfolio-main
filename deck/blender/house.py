# Smart Home Hub physical model for the Polimi deck (owner, 2026-10-31): a typical one-storey home, laid out after the
# FigJam physical-model board (entrance yard with gate and intercom, garage, day area, night area, garden), furnished in
# detail and drawn as a premium black-and-white illustration: soft daylight shading + Freestyle lines, cut walls in ink.
#   blender -b -P deck/blender/house.py -- <outdir> [view ...] [preview]     view = cut | zones | out | top (default: all)
# Writes house-<view>.png and house-anchors.json: for each view its size on the slide, a 2×4 projection matrix M (world
# metres → slide px, so the slide script can draw the board's connection network on the floor plane), artifact points,
# people, rooms and zone outlines.
import bpy, bmesh, math, json, sys, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index('--') + 1:]
OUT = os.path.abspath(argv[0])
VIEWS = [a for a in argv[1:] if a in ('cut', 'zones', 'out', 'top')] or ['cut', 'zones', 'out', 'top']
PREVIEW = 'preview' in argv
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = scene.collection

# ---------------------------------------------------------------------------------------------------------------
# Plan (metres). x = east, y = north; the street runs along the south fence (y = 0).
H_FULL, H_CUT = 3.0, 1.2
T_EXT, T_INT = 0.38, 0.16
HOUSE = (4.0, 7.0, 22.0, 20.0)
ROOMS = {
    'garage': (4.0, 7.0, 9.5, 13.5), 'hall': (9.5, 7.0, 12.5, 11.0), 'kitchen': (12.5, 7.0, 22.0, 11.0),
    'living': (9.5, 11.0, 22.0, 15.5), 'bath': (4.0, 13.5, 9.5, 20.0), 'dressing': (9.5, 15.5, 13.0, 20.0),
    'bedroom': (13.0, 15.5, 22.0, 20.0)}
ZONES = {
    'entrance': [(0.0, 0.0), (22.0, 0.0), (22.0, 7.0), (0.0, 7.0)],
    'garage': [(4.0, 7.0), (9.5, 7.0), (9.5, 13.5), (4.0, 13.5)],
    'day': [(9.5, 7.0), (22.0, 7.0), (22.0, 15.5), (9.5, 15.5)],
    'night': [(4.0, 13.5), (9.5, 13.5), (9.5, 15.5), (22.0, 15.5), (22.0, 20.0), (4.0, 20.0)],
    'garden': [(22.0, 0.0), (28.0, 0.0), (28.0, 24.0), (0.0, 24.0), (0.0, 7.0), (4.0, 7.0), (4.0, 20.0), (22.0, 20.0)]}
# exterior openings: (axis, fixed coord, from, to, sill, head)
EXT_OPEN = [('x', 7.0, 4.6, 8.9, 0.0, 2.4),      # garage door
            ('x', 7.0, 10.4, 11.6, 0.0, 2.4),    # front door
            ('x', 7.0, 13.4, 17.6, 0.9, 2.4),    # kitchen window
            ('x', 7.0, 18.6, 21.4, 0.0, 2.4),    # dining: glass door to the yard
            ('y', 22.0, 11.6, 15.0, 0.0, 2.4),   # living: sliding glass to the terrace
            ('y', 22.0, 16.2, 19.2, 0.9, 2.4),   # bedroom east
            ('x', 20.0, 15.0, 19.0, 0.9, 2.4),   # bedroom north
            ('x', 20.0, 5.4, 8.0, 1.3, 2.2),     # bath north
            ('y', 4.0, 15.0, 18.0, 1.3, 2.2)]    # bath west
INT_WALLS = [  # (x0, y0, x1, y1, opening from, to) along the wall
    (9.5, 7.0, 9.5, 13.5, 9.0, 10.0),       # garage | hall
    (4.0, 13.5, 9.5, 13.5, None, None),     # garage | bath
    (9.5, 13.5, 9.5, 20.0, 14.0, 15.0),     # bath | living, dressing
    (12.5, 7.0, 12.5, 11.0, 8.4, 10.2),     # hall | kitchen
    (9.5, 11.0, 12.5, 11.0, 10.2, 11.8),    # hall | living
    (9.5, 15.5, 22.0, 15.5, 10.4, 11.4),    # living | dressing, bedroom
    (13.0, 15.5, 13.0, 20.0, 16.6, 17.6)]   # dressing | bedroom

# the board's artifacts, where they sit (z: mounting height)
ART = {
    'remote_gar': (5.4, 5.0, 1.1), 'keys': (12.0, 6.6, 1.35), 'alarm': (13.9, 6.6, 2.7), 'security': (15.9, 6.6, 2.7),
    'remote_gate': (5.0, 2.2, 1.1), 'camera': (9.12, 0.0, 2.1), 'intercom': (14.4, -0.32, 1.45), 'gate': (12.6, 0.0, 1.0),
    'door': (11.0, 7.0, 1.2), 'garage_sw': (9.0, 8.3, 1.3), 'light_sw': (10.0, 8.9, 1.3), 'light': (11.3, 9.7, 2.8),
    'fire': (15.4, 8.4, 2.9), 'ac': (15.6, 15.3, 2.4), 'heating': (17.4, 15.3, 1.6), 'thermostat': (12.7, 13.4, 1.5),
    'router': (19.6, 11.25, 0.9), 'tv': (21.6, 13.3, 1.3), 'irrigation': (25.0, 9.0, 0.15), 'mower': (25.6, 17.6, 0.2)}
PEOPLE = {'owner_out': (7.2, 3.4, 0.0), 'guests': (15.6, -1.7, 0.0), 'owner_in': (17.0, 12.8, 0.0)}

# ---------------------------------------------------------------------------------------------------------------
# Materials: a soft white for everything (light and shadow do the modelling), ink for cut tops, dark grey for glass,
# screens and metal details, mid grey for foliage — still black and white.
def diffuse(name, v, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (v, v, v, 1); b.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.1
    return m
def flat(name, v):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (v, v, v, 1)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0]); return m
WHITE, FLOOR, LAWN = diffuse('white', 0.86), diffuse('floor', 0.80), diffuse('lawn', 0.74)
INK, DARK, LEAF, GLASS = flat('ink', 0.01), diffuse('dark', 0.10, 0.4), diffuse('leaf', 0.55), diffuse('glass', 0.62, 0.15)

FLOORS = bpy.data.collections.new('floors'); col.children.link(FLOORS)       # joints: thin grey lines
CUTZ = [None]
NOCUT = set()

def box(name, x0, y0, z0, x1, y1, z1, mat=WHITE, bevel=0.0, coll=None):
    # in the cut views, anything crossing the cut height is cut there and gets an ink top (except hanging things)
    if CUTZ[0] and z1 > CUTZ[0] > z0 and name not in NOCUT and not name.startswith(('car', 'pend', 'lamp')):
        box(name + '_cap', x0, y0, CUTZ[0], x1, y1, CUTZ[0] + 0.012, INK); z1 = CUTZ[0]; bevel = 0
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 + (v.co.x + 0.5) * (x1 - x0); v.co.y = y0 + (v.co.y + 0.5) * (y1 - y0); v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat); (coll or col).objects.link(o)
    if bevel > 0:
        md = o.modifiers.new('b', 'BEVEL'); md.width = min(bevel, (x1 - x0) / 2.1, (y1 - y0) / 2.1, (z1 - z0) / 2.1); md.segments = 4
        for p in me.polygons: p.use_smooth = True
    return o

def cyl(name, x, y, z0, z1, r, seg=32, mat=WHITE, r2=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=z1 - z0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(x, y, (z0 + z1) / 2)); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = abs(p.normal.z) < 0.5
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat); col.objects.link(o); return o

def wheel(name, x, y, z, r, w, mat=DARK):
    o = cyl(name, 0, 0, -w / 2, w / 2, r, 32, mat); o.rotation_euler = (0, math.radians(90), 0); o.location = (x, y, z); return o

def ball(name, x, y, z, r, sx=1.0, sy=1.0, sz=1.0, mat=WHITE):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=r)
    for v in bm.verts: v.co.x *= sx; v.co.y *= sy; v.co.z *= sz
    bmesh.ops.translate(bm, verts=bm.verts, vec=(x, y, z)); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat); col.objects.link(o); return o

# ---------------------------------------------------------------------------------------------------------------
def wall_run(name, ax, c, a0, a1, t, h, openings, cap):
    cuts = sorted([o for o in openings if o[0] == ax and abs(o[1] - c) < 1e-6], key=lambda o: o[2])
    segs, s = [], a0
    for o in cuts:
        segs.append((s, o[2], 0.0, h))
        if o[4] > 0: segs.append((o[2], o[3], 0.0, min(o[4], h)))
        if o[5] < h: segs.append((o[2], o[3], o[5], h))
        s = o[3]
    segs.append((s, a1, 0.0, h))
    for i, (p0, p1, z0, z1) in enumerate(segs):
        if p1 - p0 < 1e-3 or z1 - z0 < 1e-3: continue
        b = (p0, c - t / 2, z0, p1, c + t / 2, z1) if ax == 'x' else (c - t / 2, p0, z0, c + t / 2, p1, z1)
        NOCUT.add(f'{name}{i}'); box(f'{name}{i}', *b)
        if cap and z1 >= h - 1e-6: box(f'{name}{i}c', b[0], b[1], z1, b[3], b[4], z1 + 0.014, INK)

def planks(name, x0, y0, x1, y1, w=0.22, along='x', z=0.06):
    # a wooden floor: long boards with staggered joints
    n = int(round((y1 - y0 if along == 'x' else x1 - x0) / w))
    lo, hi = (x0, x1) if along == 'x' else (y0, y1)
    for i in range(n):
        a = (y0 if along == 'x' else x0) + i * w
        p, k = lo - (i * 0.83) % 2.4, 0
        while p < hi:
            q = min(p + 2.4, hi); pp = max(p, lo)
            if along == 'x': box(f'{name}{i}_{k}', pp + 0.004, a + 0.004, z - 0.02, q - 0.004, a + w - 0.004, z, FLOOR, coll=FLOORS)
            else: box(f'{name}{i}_{k}', a + 0.004, pp + 0.004, z - 0.02, a + w - 0.004, q - 0.004, z, FLOOR, coll=FLOORS)
            p = q; k += 1

def tiles(name, x0, y0, x1, y1, s=0.6, z=0.06):
    nx, ny = max(1, int(round((x1 - x0) / s))), max(1, int(round((y1 - y0) / s)))
    for i in range(nx):
        for j in range(ny):
            box(f'{name}{i}_{j}', x0 + i * (x1 - x0) / nx + 0.006, y0 + j * (y1 - y0) / ny + 0.006, z - 0.02,
                x0 + (i + 1) * (x1 - x0) / nx - 0.006, y0 + (j + 1) * (y1 - y0) / ny - 0.006, z, FLOOR, coll=FLOORS)

def chair(name, x, y, back):      # back: side of the backrest, 's' or 'n'
    for i, (u, v) in enumerate(((-0.2, -0.2), (0.2, -0.2), (-0.2, 0.2), (0.2, 0.2))): cyl(f'{name}l{i}', x + u, y + v, 0.0, 0.45, 0.018, 10, DARK)
    box(f'{name}s', x - 0.23, y - 0.23, 0.43, x + 0.23, y + 0.23, 0.48, WHITE, 0.03)
    by = y - 0.21 if back == 's' else y + 0.21
    box(f'{name}b', x - 0.22, by - 0.025, 0.48, x + 0.22, by + 0.025, 0.86, WHITE, 0.02)

def plant(name, x, y, r=0.25, h=1.2, pot=0.22):
    cyl(f'{name}p', x, y, 0.0, 0.42, pot, 24, WHITE, pot * 0.8)
    for i, (dx, dy, dz, rr) in enumerate(((0, 0, h * 0.75, r), (r * 0.7, 0.1, h * 0.6, r * 0.75), (-r * 0.6, -0.15, h * 0.65, r * 0.8), (0.05, r * 0.6, h * 0.9, r * 0.6))):
        ball(f'{name}f{i}', x + dx, y + dy, dz, rr, 1, 1, 1.1, LEAF)

def tree(name, x, y, r=1.6):
    cyl(f'{name}t', x, y, 0.0, 2.4, 0.14, 16, WHITE, 0.1)
    for i, (dx, dy, dz, rr) in enumerate(((0, 0, 3.4, r), (r * 0.55, 0.3, 3.0, r * 0.7), (-r * 0.5, -0.3, 3.1, r * 0.75), (0.2, -r * 0.45, 3.9, r * 0.6), (-0.2, r * 0.5, 3.8, r * 0.65))):
        ball(f'{name}c{i}', x + dx, y + dy, dz, rr, 1, 1, 0.9, LEAF)

def car(x, y):
    box('car_body', x - 0.9, y - 2.25, 0.25, x + 0.9, y + 2.25, 0.85, WHITE, 0.18)
    box('car_cab', x - 0.78, y - 1.0, 0.8, x + 0.78, y + 1.15, 1.42, GLASS, 0.22)
    box('car_roof', x - 0.74, y - 0.75, 1.36, x + 0.74, y + 0.95, 1.45, WHITE, 0.12)
    for i, (dx, dy) in enumerate(((-0.86, -1.45), (0.86, -1.45), (-0.86, 1.4), (0.86, 1.4))): wheel(f'car_w{i}', x + dx, y + dy, 0.33, 0.33, 0.24)

# ---------------------------------------------------------------------------------------------------------------
def build(view):
    for o in list(col.objects) + list(FLOORS.objects):
        if o.type not in ('CAMERA', 'LIGHT'): bpy.data.objects.remove(o, do_unlink=True)
    NOCUT.clear()
    cut = view in ('cut', 'zones', 'top'); h = H_CUT if cut else H_FULL
    x0, y0, x1, y1 = HOUSE
    box('lawn', -1.0, 0.0, -0.08, 29.0, 25.0, 0.0, LAWN)
    box('street', -1.0, -4.5, -0.14, 29.0, -1.6, -0.06, WHITE); box('kerb', -1.0, -1.6, -0.06, 29.0, -1.45, 0.06, WHITE)
    box('pave', -1.0, -1.45, -0.06, 29.0, 0.0, 0.02, WHITE)
    tiles('drive', 4.4, 0.0, 9.1, 7.0, 0.9, 0.04); tiles('path', 10.4, 0.0, 11.8, 7.0, 0.7, 0.04)
    box('slab', x0 - 0.1, y0 - 0.1, 0.0, x1 + 0.1, y1 + 0.1, 0.04)
    wall_run('ws', 'x', y0, x0 - T_EXT / 2, x1 + T_EXT / 2, T_EXT, h, EXT_OPEN, cut)
    wall_run('wn', 'x', y1, x0 - T_EXT / 2, x1 + T_EXT / 2, T_EXT, h, EXT_OPEN, cut)
    wall_run('ww', 'y', x0, y0 + T_EXT / 2, y1 - T_EXT / 2, T_EXT, h, EXT_OPEN, cut)
    wall_run('we', 'y', x1, y0 + T_EXT / 2, y1 - T_EXT / 2, T_EXT, h, EXT_OPEN, cut)
    if cut:
        for i, (a, b, c, d, f, g) in enumerate(INT_WALLS):
            ax = 'x' if b == d else 'y'
            opn = [(ax, b if ax == 'x' else a, f, g, 0.0, 2.2)] if f is not None else []
            wall_run(f'wi{i}', ax, b if ax == 'x' else a, a if ax == 'x' else b, c if ax == 'x' else d, T_INT, h, opn, True)
    else:
        facade()
    terrace(); site()
    if view == 'zones': return
    floors()
    if cut:
        CUTZ[0] = H_CUT; furniture(); CUTZ[0] = None

def facade():
    x0, y0, x1, y1 = HOUSE
    box('roof', x0 - 0.3, y0 - 0.3, H_FULL, x1 + 0.3, y1 + 0.3, H_FULL + 0.28)
    box('roofedge', x0 - 0.3, y0 - 0.3, H_FULL + 0.28, x1 + 0.3, y1 + 0.3, H_FULL + 0.34)
    for i, (ax, c, a, b, s, hd) in enumerate(EXT_OPEN):
        d = 0.05
        if i == 0:   # garage door: horizontal panels
            for k in range(6):
                z0 = hd * k / 6; box(f'gd{k}', a, c - d, z0 + 0.01, b, c + d, z0 + hd / 6 - 0.01, WHITE, 0.01)
            continue
        if i == 1:   # front door: solid leaf, long handle, glass side light
            box('fdoor', a, c - d, s, b - 0.35, c + d, hd); box('fside', b - 0.33, c - d, s, b, c + d, hd, GLASS)
            box('fhandle', b - 0.5, c - d - 0.04, 0.7, b - 0.47, c - d, 1.7, DARK); continue
        n = max(1, round((b - a) / 1.2))
        for k in range(n):
            p0, p1 = a + (b - a) * k / n, a + (b - a) * (k + 1) / n
            if ax == 'x': box(f'pane{i}_{k}', p0 + 0.04, c - d, s + 0.04, p1 - 0.04, c + d, hd - 0.04, GLASS)
            else: box(f'pane{i}_{k}', c - d, p0 + 0.04, s + 0.04, c + d, p1 - 0.04, hd - 0.04, GLASS)
        if s > 0:
            if ax == 'x': box(f'sill{i}', a - 0.05, c - 0.3, s - 0.05, b + 0.05, c, s)
            else: box(f'sill{i}', c, a - 0.05, s - 0.05, c + 0.3, b + 0.05, s)
    box('canopy', 9.9, 5.8, 2.7, 12.2, 7.0, 2.85)
    box('lampwall', 12.25, 6.75, 2.0, 12.4, 6.8, 2.25, DARK); box('numplate', 9.9, 6.78, 1.6, 10.15, 6.81, 1.75, DARK)

def floors():
    planks('pl_liv', 9.6, 11.1, 21.9, 15.4, along='x'); planks('pl_bed', 13.1, 15.6, 21.9, 19.9, along='y'); planks('pl_dr', 9.6, 15.6, 12.9, 19.9, along='y')
    tiles('t_kit', 12.6, 7.1, 21.9, 10.9, 0.6); tiles('t_hall', 9.6, 7.1, 12.4, 10.9, 0.6); tiles('t_bath', 4.1, 13.6, 9.4, 19.9, 0.45)

def terrace():
    for i in range(16):
        y = 11.0 + i * 0.3; box(f'deck{i}', 22.2, y + 0.01, 0.0, 25.4, y + 0.29, 0.08, WHITE, coll=FLOORS)
    for i, y in enumerate((11.6, 13.2)):
        box(f'loung{i}', 23.4, y, 0.18, 25.2, y + 0.7, 0.32, WHITE, 0.05); box(f'loungb{i}', 23.4, y, 0.32, 23.75, y + 0.7, 0.62, WHITE, 0.05)
        for j, (dx, dy) in enumerate(((23.5, y + 0.05), (25.1, y + 0.05), (23.5, y + 0.65), (25.1, y + 0.65))): cyl(f'loungl{i}{j}', dx, dy, 0.08, 0.18, 0.03, 8, DARK)
    cyl('dtab', 24.3, 12.9, 0.08, 0.45, 0.28)
    plant('tpl1', 22.6, 15.0, 0.3, 1.0, 0.25)

def site():
    # fence: low wall with bars, sliding drive gate, pedestrian gate, a pillar with intercom, camera and letterbox
    for i, (a, b) in enumerate(((0.0, 4.2), (9.3, 12.0), (14.9, 28.0))):
        box(f'fw{i}', a, -0.12, 0.0, b, 0.12, 0.6)
        box(f'fr{i}', a, -0.03, 1.55, b, 0.03, 1.6, DARK)
        n = int((b - a) / 0.14)
        for k in range(n + 1):
            xx = a + (b - a) * k / max(n, 1); box(f'fb{i}_{k}', xx - 0.012, -0.012, 0.6, xx + 0.012, 0.012, 1.55, DARK)
    box('fe', 27.9, 0.0, 0.0, 28.1, 24.0, 1.6); box('fn', -0.1, 23.9, 0.0, 28.1, 24.1, 1.6); box('fwst', -0.1, 0.0, 0.0, 0.1, 24.0, 1.6)
    for p, (a, b) in enumerate(((4.2, 4.55), (8.95, 9.3), (12.0, 12.15))): box(f'pil{p}', a, -0.25, 0.0, b, 0.25, 1.9)
    box('pilbig', 13.2, -0.3, 0.0, 14.9, 0.3, 2.1)       # the intercom pillar, beside the pedestrian gate
    box('dgate', 4.55, -0.05, 0.08, 8.95, 0.05, 1.6)
    for k in range(1, 30): xx = 4.55 + 4.4 * k / 30; box(f'dgb{k}', xx - 0.015, -0.07, 0.15, xx + 0.015, 0.07, 1.5, DARK)
    box('pgate', 12.15, -0.04, 0.08, 13.2, 0.04, 1.6)
    for k in range(1, 8): xx = 12.15 + 1.05 * k / 8; box(f'pgb{k}', xx - 0.015, -0.06, 0.15, xx + 0.015, 0.06, 1.5, DARK)
    box('icom', 14.2, -0.34, 1.2, 14.6, -0.3, 1.7, DARK); box('icomscr', 14.25, -0.35, 1.45, 14.55, -0.34, 1.62, GLASS)
    box('cam', 8.97, -0.2, 1.95, 9.27, 0.2, 2.12, WHITE, 0.04); cyl('camlens', 9.12, -0.22, 2.02, 2.06, 0.05, 16, DARK)
    box('mailbox', 13.4, -0.42, 0.9, 13.9, -0.3, 1.15, WHITE, 0.02)
    # garden: trees, hedge, a planted bed, stepping stones, sprinklers, robot mower and its dock
    for i, (x, y, r) in enumerate(((1.8, 10.5, 1.4), (2.0, 17.5, 1.7), (7.0, 22.3, 1.3), (16.0, 22.4, 1.5), (25.8, 21.5, 1.8), (26.6, 12.5, 1.3))):
        tree(f'tr{i}', x, y, r)
    box('hedge', 22.6, 0.6, 0.0, 23.6, 6.4, 1.1, LEAF, 0.35)
    box('bed1', 15.6, 1.0, 0.0, 18.4, 2.2, 0.35, WHITE, 0.02)
    for i in range(3): ball(f'shrub{i}', 16.1 + i * 0.95, 1.6, 0.55, 0.42, 1, 1, 0.8, LEAF)
    for i in range(7): box(f'step{i}', 23.0 + (i % 2) * 0.3, 7.4 + i * 0.6, 0.0, 23.6 + (i % 2) * 0.3, 7.8 + i * 0.6, 0.04, WHITE, coll=FLOORS)
    for i, (x, y) in enumerate(((24.6, 8.0), (25.4, 9.6), (26.6, 7.2), (24.4, 18.8), (26.6, 16.0))): cyl(f'spr{i}', x, y, 0.0, 0.16, 0.05, 12, DARK)
    box('mower', 25.2, 17.2, 0.02, 26.0, 17.9, 0.25, WHITE, 0.08); box('dock', 25.3, 18.1, 0.0, 25.9, 18.5, 0.42, WHITE, 0.03)
    for i, (dx, dy) in enumerate(((25.25, 17.3), (25.95, 17.3), (25.25, 17.8), (25.95, 17.8))): wheel(f'mw{i}', dx, dy, 0.09, 0.09, 0.06)

def furniture():
    # garage: car and shelving
    car(6.7, 9.9)
    box('gshelf', 4.3, 12.7, 0.0, 9.2, 13.25, 2.0)
    for k in range(1, 3): box(f'gsh{k}', 4.3, 12.7, k * 0.45, 9.2, 13.25, k * 0.45 + 0.03)
    # hall: bench, coat stand, rug
    box('hbench', 9.75, 7.6, 0.0, 10.15, 9.0, 0.46, WHITE, 0.04)
    cyl('coat', 12.15, 7.5, 0.0, 1.1, 0.03, 10, DARK)
    box('hrug', 10.5, 7.4, 0.0, 12.0, 10.4, 0.012)
    # kitchen: base units with fronts, worktop, hob, sink and tap, tall units with oven, island with stools, pendants
    for k in range(9):
        xa = 12.9 + k * 0.62; box(f'kb{k}', xa + 0.01, 7.25, 0.08, xa + 0.61, 7.85, 0.86)
    box('ktop', 12.85, 7.2, 0.86, 18.5, 7.95, 0.92)
    for k, (dx, dy) in enumerate(((16.0, 7.45), (16.3, 7.45), (16.0, 7.72), (16.3, 7.72))): cyl(f'burn{k}', dx, dy, 0.92, 0.935, 0.09, 24, DARK)
    box('sinkb', 14.0, 7.35, 0.84, 14.75, 7.8, 0.925, DARK); cyl('tap', 14.38, 7.88, 0.92, 1.18, 0.02, 10, DARK)
    for k in range(3): box(f'kt{k}', 18.6 + k * 0.62, 7.25, 0.0, 19.2 + k * 0.62, 7.9, 2.3)
    box('island', 14.2, 9.0, 0.0, 17.4, 9.9, 0.92, WHITE, 0.02)
    for k in range(4):
        cyl(f'st{k}', 14.7 + k * 0.8, 10.35, 0.0, 0.66, 0.025, 10, DARK); cyl(f'sts{k}', 14.7 + k * 0.8, 10.35, 0.66, 0.72, 0.19, 24)
    for k in range(2):
        cyl(f'pendw{k}', 15.2 + k * 1.2, 9.45, 1.9, 3.0, 0.006, 6, DARK); cyl(f'pend{k}', 15.2 + k * 1.2, 9.45, 1.65, 1.9, 0.08, 24, WHITE, 0.22)
    # dining: table, six chairs, pendant, sideboard with the router
    box('dtable', 18.9, 8.6, 0.72, 21.3, 9.7, 0.77, WHITE, 0.02)
    for k, (dx, dy) in enumerate(((19.0, 8.7), (21.2, 8.7), (19.0, 9.6), (21.2, 9.6))): box(f'dleg{k}', dx - 0.04, dy - 0.04, 0.0, dx + 0.04, dy + 0.04, 0.72)
    for k, (dx, dy, b) in enumerate(((19.4, 8.25, 's'), (20.1, 8.25, 's'), (20.8, 8.25, 's'), (19.4, 10.05, 'n'), (20.1, 10.05, 'n'), (20.8, 10.05, 'n'))): chair(f'dc{k}', dx, dy, b)
    cyl('pendd_w', 20.1, 9.15, 1.75, 3.0, 0.006, 6, DARK); cyl('pendd', 20.1, 9.15, 1.55, 1.75, 0.5, 40, WHITE, 0.08)
    box('sideb', 19.0, 11.05, 0.0, 21.0, 11.45, 0.8, WHITE, 0.02)
    box('routerbox', 19.45, 11.15, 0.8, 19.75, 11.35, 0.86, WHITE, 0.01)
    for k in range(2): cyl(f'rant{k}', 19.5 + k * 0.2, 11.3, 0.86, 1.0, 0.008, 6, DARK)
    # living: L sofa with cushions, armchair, coffee tables, rug, TV wall, bookshelf, floor lamp, plants
    box('rug', 13.2, 11.8, 0.0, 18.4, 14.9, 0.015)
    box('sofa_base', 13.4, 12.0, 0.0, 14.4, 15.0, 0.4, WHITE, 0.06); box('sofa_l', 13.4, 14.1, 0.0, 16.2, 15.0, 0.4, WHITE, 0.06)
    box('sofa_back', 13.4, 12.0, 0.4, 13.7, 15.0, 0.82, WHITE, 0.08); box('sofa_backl', 13.4, 14.75, 0.4, 16.2, 15.05, 0.82, WHITE, 0.08)
    for k in range(3): box(f'cush{k}', 13.72, 12.05 + k * 0.7, 0.4, 14.38, 12.72 + k * 0.7, 0.55, WHITE, 0.07)
    for k in range(2): box(f'cushl{k}', 14.42 + k * 0.88, 14.1, 0.4, 15.28 + k * 0.88, 14.72, 0.55, WHITE, 0.07)
    box('sofa_arm', 13.4, 11.85, 0.0, 14.4, 12.1, 0.6, WHITE, 0.08)
    box('pillow1', 13.75, 12.15, 0.55, 13.95, 12.6, 0.85, WHITE, 0.08); box('pillow2', 15.6, 14.4, 0.55, 16.05, 14.62, 0.85, WHITE, 0.08)
    cyl('ctab', 16.0, 13.2, 0.0, 0.38, 0.55, 48); cyl('ctab2', 16.6, 12.4, 0.0, 0.46, 0.3, 32)
    box('arm_base', 17.8, 11.8, 0.0, 18.6, 12.6, 0.42, WHITE, 0.08); box('arm_back', 18.35, 11.8, 0.42, 18.6, 12.6, 0.82, WHITE, 0.08)
    box('tvwall', 21.45, 12.0, 0.0, 21.8, 14.8, 0.5, WHITE, 0.02)
    box('tvscreen', 21.62, 12.45, 0.6, 21.7, 14.25, 1.15, DARK)
    box('books', 9.75, 11.3, 0.0, 10.15, 13.3, 2.0)
    for k in range(1, 3): box(f'bk{k}', 9.75, 11.3, k * 0.4, 10.15, 13.3, k * 0.4 + 0.025)
    cyl('lamp_fl', 13.2, 11.7, 0.0, 1.55, 0.015, 8, DARK); cyl('lamp_fs', 13.2, 11.7, 1.4, 1.7, 0.2, 24, WHITE, 0.12)
    plant('pl1', 21.5, 11.5, 0.35, 1.5, 0.25); plant('pl2', 10.2, 14.9, 0.3, 1.2, 0.22)
    # bedroom: bed with duvet and pillows, nightstands with lamps, bench, rug, plant
    box('brug', 15.2, 15.9, 0.0, 19.8, 18.8, 0.012)
    box('bed_frame', 15.8, 16.5, 0.0, 17.8, 19.6, 0.32, WHITE, 0.03); box('mattress', 15.85, 16.55, 0.32, 17.75, 19.55, 0.52, WHITE, 0.06)
    box('duvet', 15.8, 16.45, 0.5, 17.8, 18.6, 0.6, WHITE, 0.08); box('duvfold', 15.8, 18.4, 0.5, 17.8, 18.75, 0.64, WHITE, 0.08)
    box('headboard', 15.6, 19.6, 0.0, 18.0, 19.78, 1.1, WHITE, 0.04)
    box('bpil1', 15.95, 18.95, 0.52, 16.75, 19.45, 0.7, WHITE, 0.09); box('bpil2', 16.85, 18.95, 0.52, 17.65, 19.45, 0.7, WHITE, 0.09)
    for k, xx in enumerate((15.0, 18.2)):
        box(f'ns{k}', xx, 19.15, 0.0, xx + 0.5, 19.65, 0.5, WHITE, 0.02)
        cyl(f'lamp_n{k}', xx + 0.25, 19.4, 0.5, 0.72, 0.02, 8, DARK); cyl(f'lamp_ns{k}', xx + 0.25, 19.4, 0.72, 0.92, 0.13, 24, WHITE, 0.1)
    box('bbench', 15.9, 15.9, 0.0, 17.7, 16.3, 0.45, WHITE, 0.04)
    plant('pl3', 21.4, 19.3, 0.3, 1.3, 0.22)
    # dressing: wardrobes, island
    for k in range(4): box(f'ward{k}', 9.7, 15.9 + k * 0.95, 0.0, 10.35, 16.83 + k * 0.95, 2.3)
    box('dress_isl', 11.2, 17.0, 0.0, 12.2, 18.6, 0.9, WHITE, 0.03)
    # bath: freestanding tub, shower with glass, double vanity, toilet, plant
    box('tub', 4.5, 17.6, 0.0, 5.4, 19.4, 0.58, WHITE, 0.25); box('tub_in', 4.62, 17.75, 0.45, 5.28, 19.25, 0.585, WHITE, 0.2)
    box('shower_tray', 7.7, 18.2, 0.0, 9.3, 19.8, 0.05); box('shower_glass', 7.65, 18.15, 0.05, 9.3, 18.18, 2.0, GLASS)
    box('vanity', 4.2, 14.2, 0.35, 4.75, 16.6, 0.85, WHITE, 0.02)
    for k in range(2): box(f'basin{k}', 4.3, 14.6 + k * 1.1, 0.85, 4.68, 15.2 + k * 1.1, 0.95, WHITE, 0.08)
    box('wc', 8.6, 14.0, 0.0, 9.25, 14.45, 0.42, WHITE, 0.12); box('wc_t', 9.15, 13.95, 0.42, 9.3, 14.5, 0.8, WHITE, 0.03)
    plant('pl4', 6.8, 19.5, 0.25, 0.9, 0.18)

# ---------------------------------------------------------------------------------------------------------------
SS = 1.25 if PREVIEW else 2.0
scene.render.engine = 'CYCLES'; scene.cycles.samples = 24 if PREVIEW else 96; scene.cycles.use_denoising = True
scene.render.film_transparent = True
scene.view_settings.view_transform = 'Standard'; scene.view_settings.exposure = 0.15
w = bpy.data.worlds.new('w'); scene.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (1, 1, 1, 1); bg.inputs['Strength'].default_value = 0.55
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 3.2; sd.angle = math.radians(6)
sun = bpy.data.objects.new('sun', sd); col.objects.link(sun); sun.rotation_euler = (math.radians(48), 0, math.radians(-38))
r = scene.render; r.use_freestyle = True; r.line_thickness_mode = 'ABSOLUTE'; r.line_thickness = 1.0
vl = scene.view_layers[0]; vl.use_freestyle = True; fs = vl.freestyle_settings; fs.crease_angle = math.radians(138)
for ls in list(fs.linesets): fs.linesets.remove(ls)
def lineset(name, px, grey, floors_only, **types):
    ls = fs.linesets.new(name); ls.select_by_visibility = True; ls.visibility = 'VISIBLE'; ls.select_by_edge_types = True
    ls.select_by_collection = True; ls.collection = FLOORS; ls.collection_negation = 'INCLUSIVE' if floors_only else 'EXCLUSIVE'
    for k in ('silhouette', 'border', 'crease', 'external_contour', 'material_boundary', 'contour'): setattr(ls, 'select_' + k, types.get(k, False))
    st = ls.linestyle; st.color = (grey,) * 3; st.thickness = px; st.caps = 'ROUND'
lineset('inner', 1.15 * SS, 0.03, False, silhouette=True, border=True, crease=True, material_boundary=True, contour=True)
lineset('outline', 2.0 * SS, 0.02, False, external_contour=True)
lineset('joints', 0.55 * SS, 0.42, True, border=True, crease=True, contour=True, silhouette=True)

cd = bpy.data.cameras.new('iso'); cd.type = 'ORTHO'
cam = bpy.data.objects.new('iso', cd); col.objects.link(cam); scene.camera = cam
SIZE = {'cut': 1240, 'zones': 900, 'out': 1240, 'top': 1000}
ROT = {'cut': (54.7356, 0, 45), 'zones': (54.7356, 0, 45), 'out': (54.7356, 0, 45), 'top': (0, 0, 0)}
FRAME = (-1.2, -2.6, 29.0, 25.0)
path = os.path.join(OUT, 'house-anchors.json')
anchors = json.load(open(path)) if os.path.exists(path) else {}
for view in VIEWS:
    build(view)
    sd.energy = 1.7 if view == 'top' else 3.2; bg.inputs['Strength'].default_value = 0.85 if view == 'top' else 0.55   # softer shadows from above
    cam.rotation_euler = tuple(math.radians(a) for a in ROT[view]); bpy.context.view_layer.update()
    R = cam.matrix_world.to_3x3(); right, up, back = R.col[0], R.col[1], R.col[2]
    zt = H_FULL + 4.6 if view != 'top' else 0.0
    cs = [Vector((x, y, z)) for x in (FRAME[0], FRAME[2]) for y in (FRAME[1], FRAME[3]) for z in (0.0, zt)]
    xs = [c.dot(right) for c in cs]; ys = [c.dot(up) for c in cs]
    sx, sy = (max(xs) - min(xs)), (max(ys) - min(ys))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    cam.location = right * cx + up * cy + back * 80.0
    cd.clip_end = 300; cd.sensor_fit = 'HORIZONTAL'; cd.ortho_scale = sx
    wpx = SIZE[view]; hpx = round(wpx * sy / sx)
    scene.render.resolution_x, scene.render.resolution_y = round(wpx * SS), round(hpx * SS); scene.render.resolution_percentage = 100
    bpy.context.view_layer.update()
    def proj(p):
        v = world_to_camera_view(scene, cam, Vector(p)); return [round(v.x * wpx, 2), round((1 - v.y) * hpx, 2)]
    o, ex, ey, ez = proj((0, 0, 0)), proj((1, 0, 0)), proj((0, 1, 0)), proj((0, 0, 1))
    M = [[ex[0] - o[0], ey[0] - o[0], ez[0] - o[0], o[0]], [ex[1] - o[1], ey[1] - o[1], ez[1] - o[1], o[1]]]
    zl = 0.06
    anchors[view] = {'w': wpx, 'h': hpx, 'M': M,
        'art': {k: proj(p if view != 'top' else (p[0], p[1], 0)) for k, p in ART.items()}, 'art3': ART,
        'people': {k: proj(p) for k, p in PEOPLE.items()}, 'people3': PEOPLE,
        'rooms': {k: proj(((q[0] + q[2]) / 2, (q[1] + q[3]) / 2, zl)) for k, q in ROOMS.items()},
        'zones': {k: [proj((x, y, zl)) for x, y in pts] for k, pts in ZONES.items()}}
    scene.render.filepath = os.path.join(OUT, f'house-{view}.png')
    bpy.ops.render.render(write_still=True)
    with open(path, 'w') as f: json.dump(anchors, f, indent=1)
