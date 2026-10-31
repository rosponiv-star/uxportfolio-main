# Smart Home Hub physical model for the Polimi deck (owner, 2026-10-31): a typical one-storey home, laid out after the
# FigJam physical-model board (entrance yard with gate and intercom, garage, day area, night area, garden), drawn as an
# architect's illustration in black and white: real furniture, plants and trees (Poly Haven, CC0), real people (MPFB2 +
# MakeHuman system assets, CC0), soft daylight, light grey Freestyle lines, cut walls in ink. The connection network is
# drawn on top by the slide, dark, so it stays the focus.
#   blender -b -P deck/blender/house.py -- <outdir> [view ...] [preview]     view = cut | zones | out | top (default: all)
# Assets live in deck/blender/assets/ (git-ignored: polyhaven/<id>/<id>_1k.gltf, makehuman/ unpacked into MPFB's user data).
# Writes house-<view>.png and house-anchors.json: for each view its size on the slide, a 2×4 projection matrix M (world
# metres → slide px), artifact points, people, rooms and zone outlines.
import bpy, bmesh, math, json, sys, os
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index('--') + 1:]
OUT = os.path.abspath(argv[0])
VIEWS = [a for a in argv[1:] if a in ('cut', 'zones', 'out', 'top')] or ['cut', 'zones', 'out', 'top']
PREVIEW = 'preview' in argv
NOPEOPLE = 'nopeople' in argv
HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, 'assets', 'polyhaven')
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = scene.collection

# ---------------------------------------------------------------------------------------------------------------
# Plan (metres). x = east, y = north; the street runs along the south fence (y = 0).
# Three volumes, not one box: a low garage set back from the street, a tall day wing with a deep roof overhang over
# the entrance and the terrace, a night wing pushed west and north (the plan becomes an L, with a patio in the corner).
H_CUT = 1.2
T_EXT, T_INT = 0.38, 0.16
H_GAR, H_DAY, H_NIGHT = 2.9, 3.5, 3.1
ROOMS = {
    'garage': (4.0, 7.6, 9.5, 13.5), 'hall': (9.5, 8.2, 12.5, 11.0), 'kitchen': (12.5, 7.0, 22.0, 11.0),
    'living': (9.5, 11.0, 22.0, 15.5), 'bath': (3.0, 13.5, 9.5, 18.0), 'dressing': (3.0, 18.0, 9.5, 20.5),
    'bedroom': (9.5, 15.5, 15.5, 20.5)}
ZONES = {
    'entrance': [(0.0, 0.0), (22.0, 0.0), (22.0, 7.0), (12.5, 7.0), (12.5, 8.2), (9.5, 8.2), (9.5, 7.6), (4.0, 7.6), (0.0, 7.6)],
    'garage': [(4.0, 7.6), (9.5, 7.6), (9.5, 13.5), (4.0, 13.5)],
    'day': [(9.5, 8.2), (12.5, 8.2), (12.5, 7.0), (22.0, 7.0), (22.0, 15.5), (9.5, 15.5)],
    'night': [(3.0, 13.5), (9.5, 13.5), (9.5, 15.5), (15.5, 15.5), (15.5, 20.5), (3.0, 20.5)],
    'garden': [(22.0, 0.0), (28.0, 0.0), (28.0, 24.0), (0.0, 24.0), (0.0, 7.6), (4.0, 7.6), (4.0, 13.5), (3.0, 13.5), (3.0, 20.5),
               (15.5, 20.5), (15.5, 15.5), (22.0, 15.5)]}
# exterior walls: (axis, fixed coord, from, to, height) — axis 'x' runs along x at y = fixed
EXT = [('x', 7.6, 4.0, 9.5, H_GAR), ('y', 4.0, 7.6, 13.5, H_GAR), ('x', 13.5, 3.0, 4.0, H_NIGHT),          # garage
       ('y', 9.5, 7.6, 8.2, H_DAY), ('x', 8.2, 9.5, 12.5, H_DAY), ('y', 12.5, 7.0, 8.2, H_DAY),             # recessed porch
       ('x', 7.0, 12.5, 22.0, H_DAY), ('y', 22.0, 7.0, 15.5, H_DAY), ('x', 15.5, 15.5, 22.0, H_DAY),         # day wing
       ('y', 15.5, 15.5, 20.5, H_NIGHT), ('x', 20.5, 3.0, 15.5, H_NIGHT), ('y', 3.0, 13.5, 20.5, H_NIGHT)]   # night wing
# openings: (axis, fixed coord, from, to, sill, head)
OPEN = [('x', 7.6, 4.6, 8.9, 0.0, 2.4),      # garage door
        ('x', 8.2, 10.4, 11.6, 0.0, 2.5),    # front door
        ('x', 7.0, 13.4, 17.6, 0.9, 2.6),    # kitchen window
        ('x', 7.0, 18.4, 21.6, 0.0, 2.8),    # dining: glass to the yard
        ('y', 22.0, 11.4, 15.1, 0.0, 2.8),   # living: sliding glass to the terrace
        ('x', 15.5, 17.6, 20.8, 0.0, 2.6),   # living: glass to the patio
        ('y', 15.5, 16.2, 19.6, 0.0, 2.5),   # bedroom: glass to the patio
        ('x', 20.5, 11.0, 14.4, 0.9, 2.5),   # bedroom north
        ('x', 20.5, 4.0, 8.4, 1.0, 2.3),     # dressing north
        ('y', 3.0, 14.4, 16.8, 1.3, 2.3)]    # bath west
INT = [  # (x0, y0, x1, y1, [(from, to), …]) openings along the wall
    (9.5, 7.6, 9.5, 13.5, [(9.0, 10.0)]),            # garage | hall
    (3.0, 13.5, 9.5, 13.5, []),                      # garage | bath
    (9.5, 13.5, 9.5, 20.5, [(14.0, 15.0), (18.6, 19.6)]),   # bath, dressing | living, bedroom
    (3.0, 18.0, 9.5, 18.0, [(6.2, 7.2)]),            # bath | dressing
    (12.5, 8.2, 12.5, 11.0, [(8.6, 10.4)]),          # hall | kitchen
    (9.5, 11.0, 12.5, 11.0, [(10.2, 11.8)]),         # hall | living
    (9.5, 15.5, 15.5, 15.5, [(11.0, 12.0)])]         # living | bedroom

# the board's artifacts, where they sit (z: mounting height)
ART = {
    'remote_gar': (5.4, 5.0, 1.1), 'keys': (12.4, 7.65, 1.35), 'alarm': (14.0, 6.75, 2.9), 'security': (16.0, 6.75, 2.9),
    'remote_gate': (5.0, 2.2, 1.1), 'camera': (9.12, 0.0, 2.1), 'intercom': (14.4, -0.32, 1.45), 'gate': (12.6, 0.0, 1.0),
    'door': (11.0, 8.2, 1.2), 'garage_sw': (8.6, 9.5, 1.3), 'light_sw': (10.2, 10.6, 1.3), 'light': (11.6, 9.6, 2.8),
    'fire': (15.4, 8.4, 2.9), 'ac': (14.0, 15.3, 2.4), 'heating': (17.0, 15.3, 1.6), 'thermostat': (12.7, 13.4, 1.5),
    'router': (19.6, 11.25, 0.9), 'tv': (21.6, 13.3, 1.3), 'irrigation': (25.0, 9.0, 0.15), 'mower': (25.6, 17.6, 0.2)}
PEOPLE = {'owner_out': (7.2, 3.4, 0.0), 'guests': (15.6, -1.7, 0.0), 'owner_in': (17.0, 12.8, 0.0)}

# ---------------------------------------------------------------------------------------------------------------
# Materials: light, soft greys (the house recedes; the slide's network stays dark), ink for cut tops.
def diffuse(name, v, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (v, v, v, 1); b.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.15
    return m
def flat(name, v):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (v, v, v, 1)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0]); return m
WHITE, FLOOR, LAWN, TIMBER = diffuse('white', 0.88), diffuse('floor', 0.80), diffuse('lawn', 0.78), diffuse('timber', 0.70)
INK, DARK, GLASS, STONE = flat('ink', 0.16), diffuse('dark', 0.25, 0.4), diffuse('glass', 0.70, 0.12), diffuse('stone', 0.76)

FLOORS = bpy.data.collections.new('floors'); col.children.link(FLOORS)       # joints: thin, light lines
CUTZ = [None]
NOCUT = set()

VEG = []
def nolines(o, heavy=False):
    # vegetation and people: shading only, no Freestyle (their outlines would turn into noise); heavy meshes (trees,
    # shrubs) are swapped for light proxies in the line pass so Freestyle stays fast but they still hide what is behind
    for ob in [o] + list(o.children_recursive):
        if heavy and ob.type == 'MESH': VEG.append(ob)
        if ob.type == 'MESH':
            me = ob.data; a = me.attributes.get('freestyle_face') or me.attributes.new('freestyle_face', 'BOOLEAN', 'FACE')
            a.data.foreach_set('value', [True] * len(me.polygons))

def box(name, x0, y0, z0, x1, y1, z1, mat=WHITE, bevel=0.0, coll=None):
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

# ---------------------------------------------------------------------------------------------------------------
# Library assets (Poly Haven glTF, real-world scale). Colours become greys (texture detail kept, hue dropped).
WASH = [0.4]
def grey_materials(objs, lift=1.15):
    for o in objs:
        if o.type != 'MESH': continue
        for slot in o.material_slots:
            m = slot.material
            if not m or m.get('greyed'): continue
            m['greyed'] = True; nt = m.node_tree
            b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if not b: continue
            inp = b.inputs['Base Color']
            hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = 0.0; hs.inputs['Value'].default_value = lift
            if inp.is_linked:
                src = inp.links[0].from_socket; nt.links.new(src, hs.inputs['Color'])
            else:
                hs.inputs['Color'].default_value = inp.default_value
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['Factor'].default_value = WASH[0]
            mx.inputs['B'].default_value = (1, 1, 1, 1); nt.links.new(hs.outputs['Color'], mx.inputs['A']); nt.links.new(mx.outputs['Result'], inp)
            if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.2

def asset(aid, x, y, rot=0.0, z=0.0, scale=1.0, veg=False, cut=True, lift=1.75):
    path = os.path.join(PH, aid, f'{aid}_1k.gltf')
    if not os.path.exists(path): print('missing asset', aid); return None
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        for c in list(o.users_collection): c.objects.unlink(o)
        col.objects.link(o)
    roots = [o for o in new if o.parent is None]
    root = bpy.data.objects.new(f'A_{aid}', None); col.objects.link(root)
    for r in roots: r.parent = root
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in new if o.type == 'MESH' for c in o.bound_box]
    if pts:
        cx = (min(p.x for p in pts) + max(p.x for p in pts)) / 2; cy = (min(p.y for p in pts) + max(p.y for p in pts)) / 2; z0 = min(p.z for p in pts)
        for r in roots: r.location -= Vector((cx, cy, z0))
    root.scale = (scale,) * 3; root.rotation_euler = (0, 0, math.radians(rot)); root.location = (x, y, z)
    WASH[0] = 0.12 if veg else 0.45; grey_materials(new, lift)
    if veg: nolines(root, heavy=True)
    bpy.context.view_layer.update()
    if CUTZ[0] and cut:      # cut through the plane too: a boolean-free trick, a bisect of each mesh at the cut height
        for o in new:
            if o.type != 'MESH': continue
            mw = o.matrix_world; inv = mw.inverted()
            me = o.data.copy(); o.data = me
            bm = bmesh.new(); bm.from_mesh(me)
            co = inv @ Vector((0, 0, CUTZ[0])); no = (mw.to_3x3().transposed() @ Vector((0, 0, 1))).normalized()
            res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no, clear_outer=True)
            bm.to_mesh(me); bm.free()
    return root

# ---------------------------------------------------------------------------------------------------------------
def wall_run(name, ax, c, a0, a1, t, h, openings, cap):
    cuts = sorted([o for o in openings if o[0] == ax and abs(o[1] - c) < 1e-6 and o[2] < a1 and o[3] > a0], key=lambda o: o[2])
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

def planks(name, x0, y0, x1, y1, w=0.2, along='x', z=0.06):
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

def tiles(name, x0, y0, x1, y1, s=0.6, z=0.06, mat=None):
    nx, ny = max(1, int(round((x1 - x0) / s))), max(1, int(round((y1 - y0) / s)))
    for i in range(nx):
        for j in range(ny):
            box(f'{name}{i}_{j}', x0 + i * (x1 - x0) / nx + 0.006, y0 + j * (y1 - y0) / ny + 0.006, z - 0.02,
                x0 + (i + 1) * (x1 - x0) / nx - 0.006, y0 + (j + 1) * (y1 - y0) / ny - 0.006, z, mat or FLOOR, coll=FLOORS)

def car(x, y):
    box('car_body', x - 0.9, y - 2.25, 0.25, x + 0.9, y + 2.25, 0.85, WHITE, 0.2)
    box('car_cab', x - 0.78, y - 1.0, 0.8, x + 0.78, y + 1.15, 1.42, GLASS, 0.24)
    box('car_roof', x - 0.74, y - 0.75, 1.36, x + 0.74, y + 0.95, 1.45, WHITE, 0.14)
    for i, (dx, dy) in enumerate(((-0.86, -1.45), (0.86, -1.45), (-0.86, 1.4), (0.86, 1.4))): wheel(f'car_w{i}', x + dx, y + dy, 0.33, 0.33, 0.24)

# ---------------------------------------------------------------------------------------------------------------
# People: MPFB2 humans (MakeHuman base mesh), dressed with the system assets, posed with the default rig.
def person(name, x, y, rot, pose='stand', female=False, outfit=None):
    if NOPEOPLE: return None
    try:
        from bl_ext.user_default.mpfb.services.humanservice import HumanService
    except Exception as e:
        print('no MPFB', e); return None
    macro = {'gender': 0.0 if female else 1.0, 'age': 0.5, 'muscle': 0.5, 'weight': 0.5, 'height': 0.55 if female else 0.6}
    before = set(bpy.data.objects)
    body = HumanService.create_human(scale=0.1, macro_detail_dict={'gender': macro['gender'], 'age': macro['age'], 'muscle': macro['muscle'],
                                                                   'weight': macro['weight'], 'height': macro['height'], 'proportions': 0.5,
                                                                   'race': {'african': 0.33, 'asian': 0.33, 'caucasian': 0.34}})
    rig = HumanService.add_builtin_rig(body, 'default')
    for f in (outfit or []):
        try: HumanService.add_mhclo_asset(f, body, asset_type='Clothes' if '/clothes/' in f.replace('\\', '/') else
                                          ('Hair' if '/hair/' in f.replace('\\', '/') else ('Eyebrows' if 'eyebrow' in f else 'Clothes')), subdiv_levels=0, material_type='SIMPLE')
        except Exception as e: print('asset fail', f, e)
    pose_rig(rig, pose)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        if o.type == 'MESH':
            nm = o.name.lower(); v = 0.62 if o is body else (0.06 if ('hair' in nm or 'brow' in nm or 'bob' in nm or 'short' in nm) else (0.05 if 'shoe' in nm else (0.12 if female else 0.2)))
            o.data.materials.clear(); o.data.materials.append(diffuse(f'p_{name}_{o.name}', v, 0.8))
            for p in o.data.polygons: p.use_smooth = True
    rig.location = (x, y, 0); rig.rotation_euler = (0, 0, math.radians(rot))
    for o in new:
        nm = o.name.lower()
        if o.type == 'MESH' and ('hair' in nm or 'brow' in nm or 'bob' in nm or 'short' in nm or 'lash' in nm): nolines(o)
    return rig

def pose_rig(rig, pose):
    PB = rig.pose.bones
    for pb in PB: pb.rotation_mode = 'XYZ'
    def rot(n, x=0, y=0, z=0):
        if n in PB: PB[n].rotation_euler = (math.radians(x), math.radians(y), math.radians(z))
    # arms down from the T/A rest pose, elbows slightly bent
    rot('upperarm01.L', 0, 0, 62); rot('upperarm01.R', 0, 0, -62)
    rot('lowerarm01.L', 18, 0, 0); rot('lowerarm01.R', 18, 0, 0)
    if pose == 'phone':      # right forearm up, looking at a phone
        rot('upperarm01.R', 0, 0, -52); rot('lowerarm01.R', 100, 0, 0)
    if pose == 'sit':
        rot('upperleg01.L', -90, 0, 0); rot('upperleg01.R', -90, 0, 0); rot('lowerleg01.L', 90, 0, 0); rot('lowerleg01.R', 90, 0, 0)
    bpy.context.view_layer.update()

# ---------------------------------------------------------------------------------------------------------------
def build(view):
    for o in list(col.objects) + list(FLOORS.objects):
        if o.type not in ('CAMERA', 'LIGHT'): bpy.data.objects.remove(o, do_unlink=True)
    NOCUT.clear(); VEG.clear()
    cut = view in ('cut', 'zones', 'top')
    box('lawn', -1.0, 0.0, -0.08, 29.0, 25.0, 0.0, LAWN)
    box('street', -1.0, -4.5, -0.14, 29.0, -1.6, -0.06, WHITE); box('kerb', -1.0, -1.6, -0.06, 29.0, -1.45, 0.06, WHITE)
    box('pave', -1.0, -1.45, -0.06, 29.0, 0.0, 0.02, WHITE)
    tiles('drive', 4.4, 0.0, 9.1, 7.5, 0.9, 0.04); tiles('path', 10.3, 0.0, 11.7, 6.9, 0.7, 0.04); box('porch', 9.5, 6.9, 0.0, 12.5, 8.2, 0.06, STONE)
    box('slab1', 3.9, 7.5, 0.0, 9.5, 13.5, 0.04); box('slab2', 9.5, 6.9, 0.0, 22.1, 15.5, 0.04)
    box('slab3', 2.9, 13.5, 0.0, 9.5, 20.6, 0.04); box('slab4', 9.5, 15.5, 0.0, 15.6, 20.6, 0.04)   # abutting, never overlapping (coplanar faces render black)
    for i, (ax, c, a0, a1, hh) in enumerate(EXT):
        h = H_CUT if cut else hh
        if ax == 'x': wall_run(f'we{i}_', ax, c, a0 - T_EXT / 2, a1 + T_EXT / 2, T_EXT, h, OPEN, cut)
        else: wall_run(f'we{i}_', ax, c, a0 + T_EXT / 2, a1 - T_EXT / 2, T_EXT, h, OPEN, cut)
    if cut:
        for i, (a, b, c, d, ops) in enumerate(INT):
            ax = 'x' if b == d else 'y'; fx = b if ax == 'x' else a
            opn = [(ax, fx, f, g, 0.0, 2.2) for f, g in ops]
            wall_run(f'wi{i}_', ax, fx, a if ax == 'x' else b, c if ax == 'x' else d, T_INT, H_CUT, opn, True)
    else:
        facade()
    terrace(); site(view)
    if view == 'zones': return
    floors()
    if cut:
        CUTZ[0] = H_CUT; furniture(); CUTZ[0] = None
    if view in ('cut', 'out'):
        people(view)

def facade():
    # roofs: each volume its own slab and height; the day wing's slab overhangs the porch, the dining glass and the terrace
    box('roof_gar', 3.8, 7.4, H_GAR, 9.6, 13.7, H_GAR + 0.25)
    box('roof_day', 9.4, 5.6, H_DAY, 22.0 + 2.2, 15.7, H_DAY + 0.32)
    box('roof_day_edge', 9.4, 5.6, H_DAY + 0.32, 24.2, 15.7, H_DAY + 0.38)
    box('roof_night', 2.8, 13.3, H_NIGHT, 15.7, 20.7, H_NIGHT + 0.28)
    cyl('col1', 24.0, 11.2, 0.0, H_DAY, 0.07, 16); cyl('col2', 24.0, 15.4, 0.0, H_DAY, 0.07, 16)     # slim columns under the terrace overhang
    # garage: vertical timber slats over the whole south face, the sectional door flush within them
    for k in range(int((9.5 - 4.0) / 0.12)):
        xx = 4.0 + k * 0.12
        if 4.6 <= xx <= 8.9: continue
        box(f'slat{k}', xx + 0.01, 7.38, 0.0, xx + 0.09, 7.42, H_GAR, TIMBER)
    for k in range(10):
        z0 = 2.4 * k / 10; box(f'gd{k}', 4.6, 7.52, z0 + 0.01, 8.9, 7.58, z0 + 0.23, TIMBER)
    # night wing: a stone base course on the west face
    for r in range(8):
        for k in range(12):
            off = 0.3 if r % 2 else 0.0; y0 = 13.5 + k * 0.6 + off
            if y0 + 0.58 > 20.5: continue
            box(f'st{r}_{k}', 2.76, y0, r * 0.3, 2.81, y0 + 0.57, r * 0.3 + 0.28, STONE)
    for i, (ax, c, a, b, s, hd) in enumerate(OPEN):
        if i == 0: continue
        d = 0.05
        if i == 1:
            box('fdoor', a, c - d, s, b - 0.35, c + d, hd, TIMBER); box('fside', b - 0.33, c - d, s, b, c + d, hd, GLASS)
            box('fhandle', b - 0.5, c - d - 0.04, 0.7, b - 0.47, c - d, 1.8, DARK); continue
        n = max(1, round((b - a) / 1.3))
        for k in range(n):
            p0, p1 = a + (b - a) * k / n, a + (b - a) * (k + 1) / n
            if ax == 'x': box(f'pane{i}_{k}', p0 + 0.035, c - d, s + 0.035, p1 - 0.035, c + d, hd - 0.035, GLASS)
            else: box(f'pane{i}_{k}', c - d, p0 + 0.035, s + 0.035, c + d, p1 - 0.035, hd - 0.035, GLASS)
    box('lampwall', 12.3, 7.95, 2.0, 12.4, 8.0, 2.3, DARK); box('numplate', 9.62, 8.0, 1.6, 9.66, 8.25, 1.75, DARK)

def floors():
    planks('pl_liv', 9.6, 11.1, 21.9, 15.4, along='x'); planks('pl_bed', 9.6, 15.6, 15.4, 20.4, along='y'); planks('pl_dr', 3.1, 18.1, 9.4, 20.4, along='x')
    tiles('t_kit', 12.6, 7.1, 21.9, 10.9, 0.6); tiles('t_hall', 9.6, 8.3, 12.4, 10.9, 0.6); tiles('t_bath', 3.1, 13.6, 9.4, 17.9, 0.45)

def terrace():
    # east deck under the roof overhang, and the patio in the corner of the L (both kept clear: they read as rooms)
    for i in range(16):
        y = 11.0 + i * 0.3; box(f'deck{i}', 22.2, y + 0.01, 0.0, 25.4, y + 0.29, 0.08, WHITE, coll=FLOORS)
    tiles('patio', 15.7, 15.6, 22.0, 20.4, 0.8, 0.05)
    asset('outdoor_table_chair_set_01', 19.0, 18.2, 0, z=0.05)
    asset('vintage_day_bed', 24.2, 13.3, 90, z=0.08)
    asset('exterior_aircon_unit', 21.4, 16.0, 180)
    asset('potted_plant_04', 21.5, 20.0, veg=True); asset('potted_plant_04', 16.2, 20.0, veg=True)

def site(view):
    for i, (a, b) in enumerate(((0.0, 4.2), (9.3, 12.0), (14.9, 28.0))):
        box(f'fw{i}', a, -0.12, 0.0, b, 0.12, 0.6)
        box(f'fr{i}', a, -0.03, 1.55, b, 0.03, 1.6, DARK)
        n = int((b - a) / 0.14)
        for k in range(n + 1):
            xx = a + (b - a) * k / max(n, 1); box(f'fb{i}_{k}', xx - 0.012, -0.012, 0.6, xx + 0.012, 0.012, 1.55, DARK)
    box('fe', 27.9, 0.0, 0.0, 28.1, 24.0, 1.6); box('fn', -0.1, 23.9, 0.0, 28.1, 24.1, 1.6); box('fwst', -0.1, 0.0, 0.0, 0.1, 24.0, 1.6)
    for p, (a, b) in enumerate(((4.2, 4.55), (8.95, 9.3), (12.0, 12.15))): box(f'pil{p}', a, -0.25, 0.0, b, 0.25, 1.9)
    box('pilbig', 13.2, -0.3, 0.0, 14.9, 0.3, 2.1)
    box('dgate', 4.55, -0.05, 0.08, 8.95, 0.05, 1.6)
    for k in range(1, 30): xx = 4.55 + 4.4 * k / 30; box(f'dgb{k}', xx - 0.015, -0.07, 0.15, xx + 0.015, 0.07, 1.5, DARK)
    box('pgate', 12.15, -0.04, 0.08, 13.2, 0.04, 1.6)
    for k in range(1, 8): xx = 12.15 + 1.05 * k / 8; box(f'pgb{k}', xx - 0.015, -0.06, 0.15, xx + 0.015, 0.06, 1.5, DARK)
    box('icom', 14.2, -0.34, 1.2, 14.6, -0.3, 1.7, DARK); box('icomscr', 14.25, -0.35, 1.45, 14.55, -0.34, 1.62, GLASS)
    box('mailbox', 13.4, -0.42, 0.9, 13.9, -0.3, 1.15, WHITE, 0.02)
    asset('security_camera_01', 9.12, 0.0, 180, z=1.9)
    # garden: olive trees only along the back and the west edge (nothing in front of the house or the terrace)
    for x, y, t in ((1.8, 10.5, 'island_tree_01'), (2.0, 17.6, 'island_tree_02'), (8.0, 22.4, 'island_tree_01'), (16.0, 22.5, 'island_tree_02'),
                    (25.8, 21.5, 'island_tree_01')):
        asset(t, x, y, (x * 37) % 360, veg=True, cut=False)
    asset('planter_box_01', 12.9, 6.2, 90); asset('planter_box_01', 9.0, 6.6, 90)
    for i in range(7): box(f'step{i}', 23.0 + (i % 2) * 0.3, 7.4 + i * 0.6, 0.0, 23.6 + (i % 2) * 0.3, 7.8 + i * 0.6, 0.04, WHITE, coll=FLOORS)
    for i, (x, y) in enumerate(((25.0, 9.0), (26.4, 7.2), (24.4, 18.8), (26.6, 16.0))): asset('garden_sprinkler_01', x, y, i * 70)
    box('mower', 25.2, 17.2, 0.02, 26.0, 17.9, 0.25, WHITE, 0.08); box('dock', 25.3, 18.1, 0.0, 25.9, 18.5, 0.42, WHITE, 0.03)
    for i, (dx, dy) in enumerate(((25.25, 17.3), (25.95, 17.3), (25.25, 17.8), (25.95, 17.8))): wheel(f'mw{i}', dx, dy, 0.09, 0.09, 0.06)

def kit(name, x, y, rot=0.0, L=1.0, z=0.0, cut=True):
    # Kenney furniture kit (CC0): its models come in mixed scales, so each one is fitted to its real length L (metres)
    path = os.path.join(HERE, 'assets', 'kenney', 'furniture-kit', f'{name}.glb')
    if not os.path.exists(path): print('missing kit', name); return None
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        for c in list(o.users_collection): c.objects.unlink(o)
        col.objects.link(o)
    roots = [o for o in new if o.parent is None]
    root = bpy.data.objects.new(f'K_{name}', None); col.objects.link(root)
    for r_ in roots: r_.parent = root
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in new if o.type == 'MESH' for c in o.bound_box]
    sx = max(p.x for p in pts) - min(p.x for p in pts); sy = max(p.y for p in pts) - min(p.y for p in pts)
    cx = (min(p.x for p in pts) + max(p.x for p in pts)) / 2; cy = (min(p.y for p in pts) + max(p.y for p in pts)) / 2; z0 = min(p.z for p in pts)
    for r_ in roots: r_.location -= Vector((cx, cy, z0))
    k = L / max(sx, sy, 1e-6)
    root.scale = (k, k, k); root.rotation_euler = (0, 0, math.radians(rot)); root.location = (x, y, z)
    WASH[0] = 0.5; grey_materials(new, 1.3)
    bpy.context.view_layer.update()
    if CUTZ[0] and cut:
        for o in new:
            if o.type != 'MESH': continue
            mw = o.matrix_world; inv = mw.inverted(); me = o.data.copy(); o.data = me
            bm = bmesh.new(); bm.from_mesh(me)
            co = inv @ Vector((0, 0, CUTZ[0])); no = (mw.to_3x3().transposed() @ Vector((0, 0, 1))).normalized()
            bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no, clear_outer=True)
            bm.to_mesh(me); bm.free()
    return root

def furniture():
    # garage: the car, a stacked washer-dryer, open shelving
    car(6.75, 10.4)
    kit('washerDryerStacked', 4.5, 12.95, 0, 0.65); kit('bookcaseOpen', 6.6, 13.05, 0, 1.6); kit('bookcaseOpen', 8.3, 13.05, 0, 1.6)
    # hall: bench, doormat, coat stand
    box('hbench', 9.75, 8.6, 0.0, 10.15, 9.9, 0.46, TIMBER, 0.04)
    kit('rugDoormat', 11.0, 8.6, 0, 1.0); kit('coatRackStanding', 12.1, 8.65, 0, 0.5)
    asset('potted_plant_01', 12.1, 10.6, veg=True)
    # kitchen: base run with worktop, hob, sink; fridge column; island with bar stools; small appliances
    for k in range(9):
        xa = 12.9 + k * 0.62; box(f'kb{k}', xa + 0.01, 7.25, 0.08, xa + 0.61, 7.85, 0.86)
    box('ktop', 12.85, 7.2, 0.86, 18.2, 7.95, 0.92, STONE)
    for k, (dx, dy) in enumerate(((16.0, 7.45), (16.3, 7.45), (16.0, 7.72), (16.3, 7.72))): cyl(f'burn{k}', dx, dy, 0.92, 0.935, 0.09, 24, DARK)
    box('sinkb', 14.0, 7.35, 0.84, 14.75, 7.8, 0.925, DARK); cyl('tap', 14.38, 7.88, 0.92, 1.18, 0.02, 10, DARK)
    kit('kitchenFridgeLarge', 18.75, 7.6, 0, 0.92); kit('kitchenCoffeeMachine', 13.3, 7.55, 0, 0.32, z=0.92); kit('toaster', 17.5, 7.55, 0, 0.3, z=0.92)
    box('island', 14.2, 9.0, 0.0, 17.4, 9.9, 0.92, WHITE, 0.02); box('island_top', 14.15, 8.95, 0.92, 17.45, 9.95, 0.96, STONE)
    for k in range(4): asset('bar_chair_round_01', 14.7 + k * 0.8, 10.35, 0)
    for k in range(2):
        cyl(f'pendw{k}', 15.2 + k * 1.2, 9.45, 1.9, 3.4, 0.006, 6, DARK); cyl(f'pend{k}', 15.2 + k * 1.2, 9.45, 1.65, 1.9, 0.08, 24, WHITE, 0.22)
    # dining: table, six chairs facing it, pendant, sideboard with the router
    box('dtable', 18.9, 8.6, 0.72, 21.3, 9.7, 0.77, TIMBER, 0.02)
    for k, (dx, dy) in enumerate(((19.05, 8.75), (21.15, 8.75), (19.05, 9.55), (21.15, 9.55))): box(f'dleg{k}', dx - 0.035, dy - 0.035, 0.0, dx + 0.035, dy + 0.035, 0.72, TIMBER)
    asset('modern_ceiling_lamp_01', 20.1, 9.15, 0, z=1.7, cut=False)
    for k, (dx, dy, r_) in enumerate(((19.4, 8.3, 180), (20.1, 8.3, 180), (20.8, 8.3, 180), (19.4, 10.0, 0), (20.1, 10.0, 0), (20.8, 10.0, 0))):
        asset('dining_chair_02', dx, dy, r_)
    box('sideb', 19.0, 11.05, 0.0, 21.0, 11.45, 0.8, TIMBER, 0.02)
    box('routerbox', 19.45, 11.15, 0.8, 19.75, 11.35, 0.86, WHITE, 0.01)
    for k in range(2): cyl(f'rant{k}', 19.5 + k * 0.2, 11.3, 0.86, 1.0, 0.008, 6, DARK)
    # living
    box('rug', 13.0, 11.7, 0.0, 18.6, 14.9, 0.015)
    asset('sofa_03', 13.9, 13.2, -90)
    asset('mid_century_lounge_chair', 18.5, 12.1, 120); asset('modern_arm_chair_01', 18.4, 14.3, 60)
    asset('coffee_table_round_01', 16.0, 13.2, 0); asset('side_table_01', 13.4, 11.6, 0)
    asset('modern_wooden_cabinet', 21.55, 13.3, 90); kit('televisionModern', 21.6, 13.3, -90, 1.4, z=0.62)
    kit('bookcaseOpen', 9.85, 12.4, -90, 1.8); kit('lampSquareFloor', 13.3, 14.7, 0, 0.45)
    asset('pachira_aquatica_01', 21.4, 11.5, veg=True); asset('calathea_orbifolia_01', 10.3, 14.9, veg=True)
    # bedroom (smaller): double bed, bedside tables with lamps, a lounge chair, rug
    kit('rugRectangle', 12.5, 17.4, 0, 2.8)
    kit('bedDouble', 12.5, 19.2, 0, 2.15)
    for xx in (11.15, 13.85): kit('cabinetBedDrawerTable', xx, 20.1, 0, 0.5); kit('lampRoundTable', xx, 20.1, 0, 0.3, z=0.5)
    kit('loungeChair', 14.7, 16.3, 225, 0.85); asset('anthurium_botany_01', 15.0, 20.0, veg=True)
    # dressing: wardrobes along the north wall, an island
    for k in range(6): box(f'ward{k}', 3.3 + k * 0.95, 19.75, 0.0, 4.23 + k * 0.95, 20.35, 2.3, TIMBER)
    box('dress_isl', 5.4, 18.6, 0.0, 7.4, 19.2, 0.9, WHITE, 0.03)
    # bath (larger): bathtub, shower, double basin, toilet, cabinet
    kit('bathtub', 4.4, 17.35, 0, 1.75); kit('shower', 8.7, 17.2, 0, 1.0)
    kit('bathroomSink', 3.45, 14.2, -90, 0.6); kit('bathroomSink', 3.45, 15.0, -90, 0.6)
    kit('toilet', 9.0, 14.1, 90, 0.7); kit('bathroomCabinet', 6.0, 13.8, 0, 0.8)

def people(view):
    MH = MH_ASSETS
    m_out = [MH.get('m_clothes'), MH.get('m_shoes'), MH.get('m_hair'), MH.get('brows')]
    f_out = [MH.get('f_clothes'), MH.get('f_shoes'), MH.get('f_hair'), MH.get('brows')]
    person('owner_out', *PEOPLE['owner_out'][:2], 20, 'phone', False, [a for a in m_out if a])
    gx, gy, _ = PEOPLE['guests']
    person('guest1', gx - 0.35, gy, 10, 'stand', True, [a for a in f_out if a])
    person('guest2', gx + 0.35, gy - 0.1, -10, 'stand', False, [a for a in m_out if a])
    person('owner_in', *PEOPLE['owner_in'][:2], 200, 'stand', True, [a for a in f_out if a])

def find_mh():
    # pick the clothes, shoes, hair and eyebrows from MPFB's user data (MakeHuman system assets, CC0)
    base = os.path.join(os.environ.get('APPDATA', ''), 'Blender Foundation', 'Blender', '5.2', 'mpfb', 'data')
    found = {}
    def first(sub, keys):
        d = os.path.join(base, sub)
        if not os.path.isdir(d): return None
        for k in keys:
            for root, _, files in os.walk(d):
                for f in files:
                    if f.endswith('.mhclo') and k in f.lower(): return os.path.join(root, f)
        return None
    found['m_clothes'] = first('clothes', ['male_casualsuit04', 'male_casualsuit03', 'male_casualsuit', 'male'])
    found['f_clothes'] = first('clothes', ['female_casualsuit02', 'female_casualsuit01', 'female_casualsuit', 'female'])
    found['m_shoes'] = first('clothes', ['shoes02', 'shoes01', 'shoes'])
    found['f_shoes'] = first('clothes', ['shoes06', 'shoes05', 'shoes03', 'shoes'])
    found['m_hair'] = first('hair', ['short02', 'short04', 'short'])
    found['f_hair'] = first('hair', ['bob02', 'ponytail01', 'long01', 'bob'])
    found['brows'] = first('eyebrows', ['eyebrow001', 'eyebrow'])
    print('MH assets', found)
    return found
MH_ASSETS = find_mh()

# ---------------------------------------------------------------------------------------------------------------
SS = 1.25 if PREVIEW else 2.0
scene.render.engine = 'CYCLES'; scene.cycles.samples = 24 if PREVIEW else 96; scene.cycles.use_denoising = True
scene.render.film_transparent = True
scene.view_settings.view_transform = 'Standard'; scene.view_settings.exposure = 0.05
w = bpy.data.worlds.new('w'); scene.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (1, 1, 1, 1); bg.inputs['Strength'].default_value = 0.75
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 2.4; sd.angle = math.radians(8)
sun = bpy.data.objects.new('sun', sd); col.objects.link(sun); sun.rotation_euler = (math.radians(48), 0, math.radians(-38))
r = scene.render; r.use_freestyle = True; r.line_thickness_mode = 'ABSOLUTE'; r.line_thickness = 1.0
vl = scene.view_layers[0]; vl.use_freestyle = True; fs = vl.freestyle_settings; fs.crease_angle = math.radians(138)
for ls in list(fs.linesets): fs.linesets.remove(ls)
def lineset(name, px, grey, floors_only, **types):
    ls = fs.linesets.new(name); ls.select_by_visibility = True; ls.visibility = 'VISIBLE'; ls.select_by_edge_types = True
    ls.select_by_collection = True; ls.collection = FLOORS; ls.collection_negation = 'INCLUSIVE' if floors_only else 'EXCLUSIVE'
    ls.select_by_face_marks = True; ls.face_mark_negation = 'EXCLUSIVE'; ls.face_mark_condition = 'ONE'
    for k in ('silhouette', 'border', 'crease', 'external_contour', 'material_boundary', 'contour'): setattr(ls, 'select_' + k, types.get(k, False))
    st = ls.linestyle; st.color = (grey,) * 3; st.thickness = px; st.caps = 'ROUND'
lineset('inner', 0.85 * SS, 0.36, False, silhouette=True, border=True, crease=True, contour=True)
lineset('outline', 1.4 * SS, 0.30, False, external_contour=True)
lineset('joints', 0.45 * SS, 0.62, True, border=True, crease=True, contour=True, silhouette=True)

def combine(shade, lines, out):
    # multiply the line pass over the shading pass (alpha from the shading pass), in Blender's own image API
    import numpy as np
    a = bpy.data.images.load(shade); b = bpy.data.images.load(lines)
    pa = np.empty(len(a.pixels), np.float32); a.pixels.foreach_get(pa); pa = pa.reshape(-1, 4)
    pb = np.empty(len(b.pixels), np.float32); b.pixels.foreach_get(pb); pb = pb.reshape(-1, 4)
    pa[:, :3] *= pb[:, :3]
    ink = 1.0 - pb[:, 0]; pa[:, 3] = np.maximum(pa[:, 3], np.where(ink > 0.02, ink, 0))
    c = bpy.data.images.new('comb', a.size[0], a.size[1], alpha=True); c.pixels.foreach_set(pa.ravel())
    c.filepath_raw = out; c.file_format = 'PNG'; c.save()
cd = bpy.data.cameras.new('iso'); cd.type = 'ORTHO'
cam = bpy.data.objects.new('iso', cd); col.objects.link(cam); scene.camera = cam
SIZE = {'cut': 1700, 'zones': 1000, 'out': 1300, 'top': 1400}
ROT = {'cut': (54.7356, 0, 45), 'zones': (54.7356, 0, 45), 'out': (54.7356, 0, 45), 'top': (0, 0, 0)}
FRAME = (-1.2, -2.6, 29.0, 25.0)
path = os.path.join(OUT, 'house-anchors.json')
anchors = json.load(open(path)) if os.path.exists(path) else {}
for view in VIEWS:
    build(view)
    sd.energy = 1.5 if view == 'top' else 2.4; bg.inputs['Strength'].default_value = 1.0 if view == 'top' else 0.75
    cam.rotation_euler = tuple(math.radians(a) for a in ROT[view]); bpy.context.view_layer.update()
    R = cam.matrix_world.to_3x3(); right, up, back = R.col[0], R.col[1], R.col[2]
    zt = 8.5 if view != 'top' else 0.0
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
    # pass 1: shading only
    r.use_freestyle = False; vl.material_override = None; scene.render.film_transparent = True
    scene.render.filepath = os.path.join(OUT, f'_shade-{view}.png'); bpy.ops.render.render(write_still=True)
    # pass 2: lines only, on flat white, vegetation as light proxies
    dg = bpy.context.evaluated_depsgraph_get()
    for o in VEG:
        md = o.modifiers.new('dec', 'DECIMATE'); md.ratio = max(0.004, min(1.0, 3000 / max(1, len(o.data.polygons))))
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    for o in VEG:
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg)); o.modifiers.clear(); o.data = me
        a = me.attributes.get('freestyle_face') or me.attributes.new('freestyle_face', 'BOOLEAN', 'FACE'); a.data.foreach_set('value', [True] * len(me.polygons))
    r.use_freestyle = True; vl.material_override = flat('linebg', 1.0); scene.render.film_transparent = False
    sv = scene.cycles.samples; scene.cycles.samples = 1; scene.cycles.use_denoising = False
    scene.render.filepath = os.path.join(OUT, f'_lines-{view}.png'); bpy.ops.render.render(write_still=True)
    scene.cycles.samples = sv; scene.cycles.use_denoising = True
    combine(os.path.join(OUT, f'_shade-{view}.png'), os.path.join(OUT, f'_lines-{view}.png'), os.path.join(OUT, f'house-{view}.png'))
    with open(path, 'w') as f: json.dump(anchors, f, indent=1)
