# Smart Home Hub physical model for the Polimi deck (owner, 2026-10-31): a typical one-storey house, laid out after the
# FigJam physical-model board (entrance yard with gate and intercom, garage, day area = hall + kitchen + living, night
# area = bath + bedroom, garden), drawn in black-and-white lines like the AuraWake drawings.
#   blender -b -P deck/blender/house.py -- <outdir> [view] [preview]     view = cut | zones | out | top (default: all)
# Writes house-<view>.png (transparent, lines only, cut walls in solid ink) and house-anchors.json: for each view the
# size on the slide, the projected artifact points, people, rooms and zone outlines, so the slide script can lay icons,
# dotted leaders, labels and hatches over the drawing.
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
H_FULL, H_CUT = 2.9, 1.15          # wall height outside, cut height for the cutaway and the plan
T_EXT, T_INT = 0.36, 0.18
HOUSE = (3.0, 6.0, 15.0, 17.0)     # x0, y0, x1, y1
SITE = (-0.5, -2.4, 20.5, 19.5)
ROOMS = {                           # name: (x0, y0, x1, y1)
    'garage': (3.0, 6.0, 7.0, 12.0), 'hall': (7.0, 6.0, 9.5, 9.0), 'kitchen': (9.5, 6.0, 15.0, 9.0),
    'living': (7.0, 9.0, 15.0, 13.5), 'bath': (3.0, 12.0, 7.0, 17.0), 'bedroom': (7.0, 13.5, 15.0, 17.0)}
ZONES = {                           # the board's structure: inside = day / night area, outside = garage / garden, + the entrance yard
    'entrance': [(0.0, 0.0), (15.0, 0.0), (15.0, 6.0), (0.0, 6.0)],
    'garage': [(3.0, 6.0), (7.0, 6.0), (7.0, 12.0), (3.0, 12.0)],
    'day': [(7.0, 6.0), (15.0, 6.0), (15.0, 13.5), (7.0, 13.5)],
    'night': [(3.0, 12.0), (7.0, 12.0), (7.0, 13.5), (15.0, 13.5), (15.0, 17.0), (3.0, 17.0)],
    'garden': [(15.0, 0.0), (20.0, 0.0), (20.0, 19.0), (0.0, 19.0), (0.0, 6.0), (3.0, 6.0), (3.0, 17.0), (15.0, 17.0)]}
# openings: (wall axis 'x' or 'y', fixed coordinate, from, to, sill, head) — doors have sill 0
EXT_OPEN = [('x', 6.0, 3.5, 6.5, 0.0, 2.3),      # garage door
            ('x', 6.0, 7.75, 8.75, 0.0, 2.2),    # front door
            ('x', 6.0, 11.0, 13.6, 0.95, 2.2),   # kitchen window
            ('y', 15.0, 9.8, 12.8, 0.0, 2.2),    # living: French window to the garden
            ('y', 15.0, 14.2, 16.4, 0.95, 2.2),  # bedroom window
            ('x', 17.0, 9.0, 11.5, 0.95, 2.2),   # bedroom window north
            ('y', 3.0, 13.6, 15.0, 1.2, 2.0),    # bath window west
            ('x', 17.0, 4.0, 5.6, 1.2, 2.0)]     # bath window north
INT_WALLS = [  # (x0, y0, x1, y1, door from, door to) along the wall
    (7.0, 6.0, 7.0, 12.0, 7.0, 8.0),      # garage | hall: door into the hall
    (3.0, 12.0, 7.0, 12.0, None, None),   # garage | bath
    (7.0, 12.0, 7.0, 17.0, 12.3, 13.2),   # bath | living + bedroom
    (9.5, 6.0, 9.5, 9.0, 7.0, 8.6),       # hall | kitchen (wide opening)
    (7.0, 9.0, 9.5, 9.0, 7.6, 9.0),       # hall | living
    (9.5, 9.0, 15.0, 9.0, 10.0, 13.0),    # kitchen | living (open)
    (7.0, 13.5, 15.0, 13.5, 8.0, 9.0)]    # living | bedroom

# artifact anchors (from the board): name -> 3D point
ART = {
    'gate': (8.4, 0.0, 1.0), 'drive_gate': (5.0, 0.0, 1.0), 'intercom': (9.75, 0.05, 1.35), 'camera': (9.75, 0.0, 2.15),
    'keypad': (9.0, 5.85, 1.35), 'alarm': (12.2, 5.9, 2.55), 'security': (7.35, 5.9, 2.45), 'remote': (1.9, 3.2, 1.05),
    'garage_switch': (6.6, 6.25, 1.15), 'light_switch': (7.15, 8.3, 1.15), 'light': (8.25, 7.5, 1.15),
    'fire_alarm': (12.8, 7.6, 1.15), 'ac': (11.0, 13.35, 1.15), 'heating': (14.8, 9.6, 1.15), 'thermostat': (7.15, 11.0, 1.15),
    'router': (8.0, 9.35, 0.85), 'tv': (14.75, 11.3, 1.0), 'irrigation': (18.6, 8.0, 0.1), 'mower': (19.5, 14.0, 0.25)}
PEOPLE = {'owner_out': (2.2, 2.6, 0.0), 'guests': (10.6, -1.3, 0.0), 'owner_in': (11.6, 10.6, 0.0)}

# ---------------------------------------------------------------------------------------------------------------
# Materials: flat white everywhere (lines come from Freestyle), solid ink on cut wall tops.
def emit(name, v):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (v, v, v, 1); e.inputs['Strength'].default_value = 1
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0])
    return m
WHITE, INK, PAPER2 = emit('white', 1.0), emit('ink', 0.012), emit('paper2', 0.93)

CUTZ = [None]
def box(name, x0, y0, z0, x1, y1, z1, mat=WHITE, parent=None):
    if CUTZ[0] and z1 > CUTZ[0] and z0 < CUTZ[0] and mat is WHITE and name[:1] not in 'wf' and name not in ('ground', 'car', 'carcab'):
        box(name + 'cap', x0, y0, CUTZ[0], x1, y1, CUTZ[0] + 0.012, INK); z1 = CUTZ[0]
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 + (v.co.x + 0.5) * (x1 - x0); v.co.y = y0 + (v.co.y + 0.5) * (y1 - y0); v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat); col.objects.link(o)
    if parent: o.parent = parent
    return o

def cyl(name, x, y, z0, z1, r, seg=24, mat=WHITE):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=z1 - z0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(x, y, (z0 + z1) / 2))
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat); col.objects.link(o); return o

def blob(name, x, y, z, r, sz=1.0, mat=WHITE):     # tree crowns: a smooth sphere, only its outline is drawn
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=r)
    for v in bm.verts: v.co.z *= sz
    bmesh.ops.translate(bm, verts=bm.verts, vec=(x, y, z)); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat); col.objects.link(o); return o

def wall_run(name, ax, c, a0, a1, t, h, openings, cap):
    # one straight wall as boxes between its openings; a window keeps its sill below and a lintel above (if h allows)
    cuts = sorted([o for o in openings if o[0] == ax and abs(o[1] - c) < 1e-6], key=lambda o: o[2])
    segs, s = [], a0
    for o in cuts:
        segs.append((s, o[2], 0.0, h))
        if o[4] > 0: segs.append((o[2], o[3], 0.0, min(o[4], h)))          # sill
        if o[5] < h: segs.append((o[2], o[3], o[5], h))                     # lintel
        s = o[3]
    segs.append((s, a1, 0.0, h))
    for i, (p0, p1, z0, z1) in enumerate(segs):
        if p1 - p0 < 1e-3 or z1 - z0 < 1e-3: continue
        if ax == 'x': b = (p0, c - t / 2, z0, p1, c + t / 2, z1)
        else: b = (c - t / 2, p0, z0, c + t / 2, p1, z1)
        box(f'{name}{i}', *b)
        if cap and z1 >= h - 1e-6: box(f'{name}{i}cap', b[0], b[1], z1, b[3], b[4], z1 + 0.012, INK)

def build(view):
    for o in list(col.objects):
        if o.type != 'CAMERA': bpy.data.objects.remove(o, do_unlink=True)
    cut = view in ('cut', 'zones', 'top'); h = H_CUT if cut else H_FULL
    x0, y0, x1, y1 = HOUSE
    box('ground', SITE[0], SITE[1], -0.06, SITE[2], SITE[3], 0.0, WHITE)
    box('slab', x0 - 0.05, y0 - 0.05, 0.0, x1 + 0.05, y1 + 0.05, 0.04)
    # exterior walls
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
        # roof: flat, with a parapet; door and window frames as thin panels set back in the openings
        box('roof', x0 - T_EXT / 2, y0 - T_EXT / 2, H_FULL, x1 + T_EXT / 2, y1 + T_EXT / 2, H_FULL + 0.12)
        for nm, b in (('ps', (x0 - T_EXT / 2, y0 - T_EXT / 2, x1 + T_EXT / 2, y0 + 0.05)), ('pn', (x0 - T_EXT / 2, y1 - 0.05, x1 + T_EXT / 2, y1 + T_EXT / 2)),
                      ('pw', (x0 - T_EXT / 2, y0 - T_EXT / 2, x0 + 0.05, y1 + T_EXT / 2)), ('pe', (x1 - 0.05, y0 - T_EXT / 2, x1 + T_EXT / 2, y1 + T_EXT / 2))):
            box(nm, b[0], b[1], H_FULL + 0.12, b[2], b[3], H_FULL + 0.45)
        for i, (ax, c, a, b, s, hd) in enumerate(EXT_OPEN):
            d = 0.06
            if ax == 'x': box(f'pane{i}', a, c - d, s, b, c + d, hd)
            else: box(f'pane{i}', c - d, a, s, c + d, b, hd)
            n = 1 if i == 0 else max(1, round((b - a) / 1.3))      # mullions
            for k in range(1, n):
                m = a + (b - a) * k / n
                if ax == 'x': box(f'mul{i}{k}', m - 0.03, c - 0.09, s, m + 0.03, c + 0.02, hd)
                else: box(f'mul{i}{k}', c - 0.02, m - 0.03, s, c + 0.09, m + 0.03, hd)
        for k in range(1, 6):                                     # garage door: panels
            z = 2.3 * k / 6; box(f'gd{k}', 3.5, 5.86, z - 0.015, 6.5, 5.9, z + 0.015)
        box('canopy', 7.4, 5.0, 2.45, 9.1, 6.0, 2.55)             # over the front door
    # site: fence with two gates and a pillar for intercom, camera and keypad; paved drive and path
    box('drive', 3.3, 0.0, 0.0, 6.7, 6.0, 0.03, WHITE); box('path', 7.8, 0.0, 0.0, 8.9, 6.0, 0.03, WHITE)
    box('walk', SITE[0], SITE[1] + 0.3, 0.0, SITE[2], -0.25, 0.02)
    fence = [(0.0, 3.0), (6.8, 7.5), (9.95, 15.0), (15.0, 20.0)]
    for i, (a, b) in enumerate(fence):
        box(f'fw{i}', a, -0.1, 0.0, b, 0.1, 0.55)
        n = int((b - a) / 0.16)
        box(f'fr{i}', a, -0.03, 1.45, b, 0.03, 1.5)
        for k in range(n + 1):
            xx = a + (b - a) * k / max(n, 1); box(f'fb{i}_{k}', xx - 0.015, -0.015, 0.55, xx + 0.015, 0.015, 1.45)
    box('fwe', 19.9, 0.0, 0.0, 20.1, 19.0, 1.1); box('fwn', -0.1, 18.9, 0.0, 20.1, 19.1, 1.1); box('fww', -0.1, 0.0, 0.0, 0.1, 19.0, 1.1)
    for p, (a, b) in enumerate(((3.0, 3.35), (6.45, 6.8), (7.5, 7.75), (8.75, 9.95))):     # gate pillars; the last holds intercom and camera
        box(f'pil{p}', a, -0.22, 0.0, b, 0.22, 1.85)
    box('drgate', 3.4, -0.04, 0.05, 6.4, 0.04, 1.5)            # sliding drive gate: one leaf
    for k in range(1, 15): xx = 3.4 + 3.0 * k / 15; box(f'dg{k}', xx - 0.02, -0.06, 0.15, xx + 0.02, 0.06, 1.4)
    box('pgate', 7.75, -0.03, 0.05, 8.75, 0.03, 1.5)
    for k in range(1, 6): xx = 7.75 + k / 6; box(f'pg{k}', xx - 0.02, -0.05, 0.15, xx + 0.02, 0.05, 1.4)
    box('icom', 9.6, -0.27, 1.2, 9.9, -0.24, 1.55); box('cam', 9.62, -0.32, 1.9, 9.88, -0.05, 2.0)
    # garden: trees, a hedge, the robot mower dock and sprinklers
    for i, (x, y, r) in enumerate(((1.4, 9.0, 1.1), (1.5, 15.0, 1.3), (17.6, 17.6, 1.2), (18.6, 12.2, 1.0))):
        cyl(f'trunk{i}', x, y, 0.0, 2.2 + r * 0.6, 0.13, 12)
        blob(f'crown{i}', x, y, 2.2 + r * 1.2, r, 0.95)
    box('hedge', 15.6, 0.4, 0.0, 16.4, 5.4, 1.0)
    box('mower', 19.1, 13.7, 0.0, 19.9, 14.3, 0.25); box('dock', 19.2, 14.5, 0.0, 19.8, 14.9, 0.4)
    for i, (x, y) in enumerate(((18.0, 7.0), (18.6, 8.0), (20.4, 6.4), (17.4, 12.8))): cyl(f'spr{i}', x, y, 0.0, 0.18, 0.06, 10)
    if view == 'zones': return
    if view in ('cut', 'top'):
        CUTZ[0] = H_CUT; furniture(); CUTZ[0] = None
    # people are drawn on the slide (line figures at the projected PEOPLE points)

def furniture():
    # garage: a car
    box('car', 4.1, 7.0, 0.15, 5.9, 11.4, 0.85); box('carcab', 4.25, 8.4, 0.85, 5.75, 10.6, 1.35)
    box('shelf', 3.2, 11.3, 0.0, 6.8, 11.8, 1.0)
    # hall: console with the router, coat bench
    box('console', 7.3, 8.5, 0.0, 8.9, 8.85, 0.8); box('bench', 7.15, 6.5, 0.0, 7.55, 7.7, 0.45)
    # kitchen: counter with sink and hob along the south wall, tall unit east, table
    box('counter', 9.8, 6.15, 0.0, 14.6, 6.8, 0.9); box('hob', 12.3, 6.3, 0.9, 13.1, 6.7, 0.92); box('sink', 10.4, 6.3, 0.86, 11.1, 6.7, 0.9)
    box('tall', 14.2, 6.9, 0.0, 14.85, 8.8, 2.2); box('island', 11.0, 7.6, 0.0, 13.0, 8.4, 0.9)
    # living: sofa facing the TV, coffee table, TV unit; dining table with chairs
    box('sofa', 10.6, 10.0, 0.0, 11.5, 12.6, 0.42); box('sofaback', 10.6, 10.0, 0.42, 10.85, 12.6, 0.82)
    box('sofaarm1', 10.6, 10.0, 0.42, 11.5, 10.2, 0.6); box('sofaarm2', 10.6, 12.4, 0.42, 11.5, 12.6, 0.6)
    box('ctable', 12.2, 10.7, 0.0, 13.0, 11.9, 0.38); box('tvunit', 14.3, 10.4, 0.0, 14.8, 12.2, 0.45); box('tvpanel', 14.6, 10.6, 0.45, 14.66, 12.0, 1.1)
    box('rug', 11.8, 10.2, 0.0, 13.6, 12.4, 0.015)
    box('dtable', 7.9, 10.2, 0.72, 9.5, 11.6, 0.76)
    for i, (x, y) in enumerate(((8.0, 10.2), (8.0, 11.6), (9.4, 10.2), (9.4, 11.6))): box(f'leg{i}', x - 0.04, y - 0.04, 0.0, x + 0.04, y + 0.04, 0.72)
    for i, (x, y) in enumerate(((8.3, 9.8), (9.1, 9.8), (8.3, 12.0), (9.1, 12.0))):
        box(f'ch{i}', x - 0.22, y - 0.22, 0.0, x + 0.22, y + 0.22, 0.45)
        yb = y - 0.22 if y < 11 else y + 0.17; box(f'chb{i}', x - 0.22, yb, 0.45, x + 0.22, yb + 0.05, 0.9)
    # bedroom: bed, nightstands, wardrobe
    box('bed', 10.1, 14.6, 0.0, 12.1, 16.85, 0.5); box('headb', 10.0, 16.75, 0.0, 12.2, 16.88, 1.0)
    box('pil1', 10.25, 16.2, 0.5, 11.0, 16.65, 0.62); box('pil2', 11.2, 16.2, 0.5, 11.95, 16.65, 0.62); box('duvet', 10.1, 14.6, 0.5, 12.1, 15.8, 0.56)
    box('ns1', 9.5, 16.4, 0.0, 9.95, 16.85, 0.5); box('ns2', 12.25, 16.4, 0.0, 12.7, 16.85, 0.5)
    box('robe', 7.15, 14.0, 0.0, 7.75, 16.6, 2.1)
    # bath: shower tray, toilet, washbasin unit, bathtub
    box('tray', 3.2, 15.6, 0.0, 4.6, 16.85, 0.08); box('tub', 3.2, 12.2, 0.0, 4.0, 13.9, 0.55)
    box('wc', 5.5, 16.3, 0.0, 5.9, 16.85, 0.42); box('wctank', 5.45, 16.7, 0.42, 5.95, 16.85, 0.8)
    box('basin', 6.3, 14.4, 0.0, 6.85, 15.6, 0.85)

def person(name, x, y, n):
    # a simple standing figure (body, head) — enough at this scale; two side by side for the guests
    for k in range(n):
        dx = k * 0.6
        cyl(f'{name}{k}b', x + dx, y, 0.0, 1.4, 0.2, 16)
        blob(f'{name}{k}h', x + dx, y, 1.6, 0.14)

# ---------------------------------------------------------------------------------------------------------------
def freestyle(px_inner, px_outline):
    r = scene.render; r.use_freestyle = True; r.line_thickness_mode = 'ABSOLUTE'; r.line_thickness = 1.0
    vl = scene.view_layers[0]; vl.use_freestyle = True; fs = vl.freestyle_settings
    fs.crease_angle = math.radians(138)
    for ls in list(fs.linesets): fs.linesets.remove(ls)
    def lineset(name, px, **types):
        ls = fs.linesets.new(name); ls.select_by_visibility = True; ls.visibility = 'VISIBLE'; ls.select_by_edge_types = True
        for k in ('silhouette', 'border', 'crease', 'external_contour', 'material_boundary', 'contour'):
            setattr(ls, 'select_' + k, types.get(k, False))
        st = ls.linestyle; st.color = (0.02, 0.02, 0.02); st.thickness = px; st.caps = 'ROUND'
    lineset('inner', px_inner, silhouette=True, border=True, crease=True, material_boundary=True, contour=True)
    lineset('outline', px_outline, external_contour=True)

scene.render.engine = 'CYCLES'; scene.cycles.samples = 4 if PREVIEW else 16; scene.cycles.use_denoising = False
scene.render.film_transparent = True
scene.view_settings.view_transform = 'Standard'
w = bpy.data.worlds.new('w'); scene.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
cd = bpy.data.cameras.new('iso'); cd.type = 'ORTHO'
cam = bpy.data.objects.new('iso', cd); col.objects.link(cam); scene.camera = cam

SS = 1.25 if PREVIEW else 2.5
SIZE = {'cut': 1240, 'zones': 760, 'out': 1240, 'top': 900}     # width on the slide (px)
ROT = {'cut': (54.7356, 0, 45), 'zones': (54.7356, 0, 45), 'out': (54.7356, 0, 45), 'top': (0, 0, 0)}
path = os.path.join(OUT, 'house-anchors.json')
anchors = json.load(open(path)) if os.path.exists(path) else {}
for view in VIEWS:
    build(view)
    cam.rotation_euler = tuple(math.radians(a) for a in ROT[view]); bpy.context.view_layer.update()
    R = cam.matrix_world.to_3x3(); right, up, back = R.col[0], R.col[1], R.col[2]
    zt = H_FULL + 3.5 if view == 'out' else 2.2
    cs = [Vector((x, y, z)) for x in (SITE[0], SITE[2]) for y in (SITE[1], SITE[3]) for z in (0.0, zt)]
    xs = [c.dot(right) for c in cs]; ys = [c.dot(up) for c in cs]
    sx, sy = (max(xs) - min(xs)) * 1.02, (max(ys) - min(ys)) * 1.02
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    cam.location = right * cx + up * cy + back * 60.0
    cd.clip_end = 200
    wpx = SIZE[view]; hpx = round(wpx * sy / sx)
    scene.render.resolution_x, scene.render.resolution_y = round(wpx * SS), round(hpx * SS)
    scene.render.resolution_percentage = 100
    cd.sensor_fit = 'HORIZONTAL'; cd.ortho_scale = sx
    freestyle(1.4 * SS, 2.8 * SS)                  # 1.4 / 2.8 px as shown on the slide
    bpy.context.view_layer.update()
    def proj(p):
        v = world_to_camera_view(scene, cam, Vector(p)); return [round(v.x * wpx, 1), round((1 - v.y) * hpx, 1)]
    zl = 0.05
    anchors[view] = {'w': wpx, 'h': hpx,
        'art': {k: proj(p if view != 'top' else (p[0], p[1], H_CUT)) for k, p in ART.items()},
        'people': {k: proj(p) for k, p in PEOPLE.items()},
        'rooms': {k: proj(((r[0] + r[2]) / 2, (r[1] + r[3]) / 2, zl)) for k, r in ROOMS.items()},
        'zones': {k: [proj((x, y, zl)) for x, y in pts] for k, pts in ZONES.items()}}
    scene.render.filepath = os.path.join(OUT, f'house-{view}.png')
    bpy.ops.render.render(write_still=True)
with open(path, 'w') as f: json.dump(anchors, f, indent=1)
