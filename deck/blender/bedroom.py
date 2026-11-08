# AuraWake · one night in a bedroom (owner, 2026-11-08: real room, real window onto a real outside, light true to the hour
# and to its source). One fixed camera; only the light changes. Early May in Milan, the window faces north, so the dawn
# reaches the room as soft sky light, no direct sun. Frames (spec §6):
#   1 22:00 take the bracelet: lamp 2200 K 40 %, violet ring, shutters closing, night outside, the bed still empty
#   2 22:40 asleep: everything off, shutters closed
#   3 03:12 awake for a moment: the time on, dim and warm
#   4 06:14 the wake-up: lamp low (owner: less strong than the spec's ramp) 2800 K, shutters 20 %, amber ring
#   5 06:20 a palm on the base: lamp ~62 % 4400 K, shutters 65 % (owner: a little later and brighter)
# Loaded by aura.py (exec) in real mode: shots room1 … room5. Base at the origin, the nightstand top at z = 0.
# Materials: Poly Haven CC0 in deck/blender/assets/polyhaven_tex (git-ignored).
import random
from mathutils import noise
DAWN_LED = '#f2b53a'                    # the ring in the morning, a little yellower than DAWN (owner, 2026-11-09)
FRAME = int(SHOT[4]) if SHOT.startswith('room') and SHOT[4:].isdigit() else 0
ROOM = {   # time, lamp (share of 14 W, kelvin), ring colour or None, shutter open 0–1, exposure, sky: 'night' or sun elevation in degrees
    1: ('22:00', (0.40, 2200), NIGHT, 0.55, 0.65, 'night'),
    2: ('', (0.0, 2200), None, 0.0, 1.6, 'night'),
    3: ('03:12', (0.0, 1800), None, 0.0, 1.6, 'night'),
    4: ('06:14', (0.13, 2800), DAWN_LED, 0.20, 1.2, 1.0),
    5: ('06:20', (0.62, 4400), DAWN_LED, 0.65, 0.85, 2.4),
}
RELAX_X, RELAX_Y, RELAX_ROLL = -0.465, -0.09, 12.0
LED_W = {1: 20000.0, 4: 16000.0, 5: 18000.0}          # emission of the strip under the base: the bright contact line
LED_SPILL = {1: 55.0, 4: 38.0, 5: 62.0}                # emission of the light that leaves the gap all along the base's edge: the soft halo
TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'polyhaven_tex')
FLOOR_Z, CEIL_Z, WALL_Y = -0.50, 2.20, 0.39
BASE_ROT = math.radians(-38)                     # the base turned to the bed (owner, 2026-11-08): the time faces the pillow and the camera at about the same angle
WIN = (-0.22, 1.00, -0.05, 1.75)      # window opening: x0, x1, z0, z1
BED_R, BED_TOP, DUVET_Y = -0.30, 0.02, 0.02

def pbr(name, folder, size, tint=None, rot=0.0, bump=0.25, rough=1.0, sheen=0.0, flat=None):
    """Poly Haven maps, box-projected in object space, so no UVs are needed; size = metres covered by one tile."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    nt.links.new(tc.outputs['Object'], mp.inputs[0]); mp.inputs['Scale'].default_value = (1 / size, 1 / size, 1 / size); mp.inputs['Rotation'].default_value = (0, 0, rot)
    def tex(kind, cs):
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(os.path.join(TEX, folder, kind + '.jpg'), check_existing=True)
        n.image.colorspace_settings.name = cs; n.projection = 'BOX'; n.projection_blend = 0.2; nt.links.new(mp.outputs[0], n.inputs[0]); return n
    d = tex('diff', 'sRGB'); r = tex('rough', 'Non-Color')
    if flat is not None: b.inputs['Base Color'].default_value = flat
    elif tint is not None:
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
        nt.links.new(d.outputs[0], mx.inputs[6]); mx.inputs[7].default_value = tint; nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    else: nt.links.new(d.outputs[0], b.inputs['Base Color'])
    mt = nt.nodes.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = rough; nt.links.new(r.outputs[0], mt.inputs[0]); nt.links.new(mt.outputs[0], b.inputs['Roughness'])
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(d.outputs[0], bw.inputs[0])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = size * 0.01
    nt.links.new(bw.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs[0], b.inputs['Normal'])
    if sheen: b.inputs['Sheen Weight'].default_value = sheen
    return m

def mat_room():
    white = srgb('#f4efe6')
    MATS['wall'] = pbr('wall', 'painted_plaster_wall', 1.6, flat=srgb('#ebe4d8'), bump=0.08)
    MATS['ceil'] = principled('ceil', srgb('#efebe3'), rough=0.9)
    MATS['floor'] = pbr('floor', 'wood_floor', 1.8, rot=math.pi / 2, bump=0.15, rough=0.8)
    MATS['oak'] = pbr('oak', 'oak_veneer_01', 0.75, rot=math.pi / 2, bump=0.08, rough=0.8)
    MATS['linen'] = pbr('linen', 'rough_linen', 0.5, flat=srgb('#ded7ca'), bump=0.35, sheen=0.4)
    MATS['linen2'] = pbr('linen2', 'rough_linen', 0.5, flat=srgb('#a99c88'), bump=0.35, sheen=0.4)
    MATS['cotton'] = pbr('cotton', 'cotton_jersey', 0.22, tint=(0.42, 0.45, 0.52, 1), bump=0.4, sheen=0.5)
    MATS['wframe'] = principled('wframe', white, rough=0.42)
    MATS['slat'] = principled('slat', srgb('#b9b6af'), rough=0.5)
    MATS['brass'] = principled('brass', srgb('#a88a58'), metal=1.0, rough=0.35)
    MATS['lampmetal'] = principled('lampmetal', srgb('#23201d'), metal=0.6, rough=0.45)
    MATS['asphalt'] = principled('asphalt', srgb('#55524e'), rough=0.9)
    MATS['facade'] = pbr('facade', 'painted_plaster_wall', 4.0, flat=srgb('#d8c6ac'), bump=0.1)
    MATS['facade2'] = pbr('facade2', 'painted_plaster_wall', 4.0, flat=srgb('#bdb6aa'), bump=0.1)
    MATS['win_dark'] = principled('win_dark', srgb('#20262e'), metal=0.2, rough=0.12)
    MATS['win_lit'] = emit('win_lit', srgb('#ffc98c'), 1.2)
    # glass: light passes, a faint reflection stays
    g = bpy.data.materials.new('glass'); g.use_nodes = True; nt = g.node_tree; out = nt.nodes['Material Output']
    nt.nodes.remove(nt.nodes['Principled BSDF']); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); gl = nt.nodes.new('ShaderNodeBsdfGlossy')
    gl.inputs['Roughness'].default_value = 0.02; mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.017
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(gl.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0]); MATS['glass'] = g
    # the lamp's shade: fabric that lets the light through
    s = bpy.data.materials.new('shade'); s.use_nodes = True; nt = s.node_tree; out = nt.nodes['Material Output']; p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = srgb('#efe6d6'); p.inputs['Roughness'].default_value = 0.9
    tl = nt.nodes.new('ShaderNodeBsdfTranslucent'); tl.inputs[0].default_value = srgb('#b09a7c'); mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.45
    nt.links.new(p.outputs[0], mx.inputs[1]); nt.links.new(tl.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0]); MATS['shade'] = s
    skin = principled('skin', srgb('#d8a689'), rough=0.5); sk = skin.node_tree.nodes['Principled BSDF']
    sk.inputs['Subsurface Weight'].default_value = 0.35; sk.inputs['Subsurface Radius'].default_value = (0.012, 0.005, 0.003)
    MATS['skin'] = skin

def led_spill(color, strength):
    """The light that leaves the 2 mm gap: the strip fills the gap with bounced light and it spills out all along the base's edge.
    A row of tiny point lights hugging the footprint (lights, not meshes: a thin emitter here left a band on the base's sides),
    a little stronger at the middle of each side, nearer the round strip. strength = radiance of the source they stand for."""
    a, t, z0, step = W / 2 + 0.0016, 0.0016, 0.012, 0.005
    n_ = int(round(2 * a / step)); c, sn = math.cos(BASE_ROT), math.sin(BASE_ROT); obs = []
    for side in range(4):
        for i in range(n_):
            u = -a + (i + 0.5) * step; x, y = {0: (u, -a), 1: (a, u), 2: (-u, a), 3: (-a, -u)}[side]
            P = 4 * math.pi * strength * 2 * t * step * math.exp(-(math.hypot(x, y) - W / 2) / 0.03)
            ld = bpy.data.lights.new(f'spill{side}_{i}', 'POINT'); ld.color = color[:3]; ld.energy = P; ld.shadow_soft_size = 0.005
            o = bpy.data.objects.new(ld.name, ld); col.objects.link(o); o.location = (x * c - y * sn, x * sn + y * c, z0); o.visible_camera = False; obs.append(o)
    return obs

def only_on_the_wood(*obs):
    """Light linking: the strip lights the nightstand's top and nothing else, so its grazing rays draw no line across the room."""
    c = bpy.data.collections.new('led_receivers'); c.objects.link(bpy.data.objects['stand_top'])
    for ob in obs: ob.light_linking.receiver_collection = c

def box(name, x0, x1, y0, y1, z0, z1, mat, r=0.0, e=0.0, sp=1, se=1):
    return rbox(name, x1 - x0, y1 - y0, z1 - z0, r, e, mat, ((x0 + x1) / 2, (y0 + y1) / 2, z0), sp=sp, se=se)

def build_shell():
    """Floor, ceiling, walls with a real opening, skirting."""
    x0, x1, y0 = -3.0, 2.2, -3.2; wt = 0.22; wx0, wx1, wz0, wz1 = WIN
    box('floor', x0, x1, y0, WALL_Y + wt, FLOOR_Z - 0.05, FLOOR_Z, 'floor')
    box('ceil', x0, x1, y0, WALL_Y + wt, CEIL_Z, CEIL_Z + 0.05, 'ceil')
    box('wall_l', x0 - wt, x0, y0, WALL_Y + wt, FLOOR_Z, CEIL_Z, 'wall'); box('wall_r', x1, x1 + wt, y0, WALL_Y + wt, FLOOR_Z, CEIL_Z, 'wall')
    box('wall_f', x0, x1, y0 - wt, y0, FLOOR_Z, CEIL_Z, 'wall')
    box('back_l', x0, wx0, WALL_Y, WALL_Y + wt, FLOOR_Z, CEIL_Z, 'wall'); box('back_r', wx1, x1, WALL_Y, WALL_Y + wt, FLOOR_Z, CEIL_Z, 'wall')
    box('back_b', wx0, wx1, WALL_Y, WALL_Y + wt, FLOOR_Z, wz0, 'wall'); box('back_t', wx0, wx1, WALL_Y, WALL_Y + wt, wz1, CEIL_Z, 'wall')
    box('skirt', x0, x1, WALL_Y - 0.014, WALL_Y, FLOOR_Z, FLOOR_Z + 0.09, 'wframe', e=0.003, se=2)
    box('sill', wx0 - 0.04, wx1 + 0.04, WALL_Y - 0.04, WALL_Y + 0.14, wz0 - 0.03, wz0, 'wframe', e=0.004, se=2)

def build_window(shut):
    """A two-leaf window with its frame and handles, glass, and the roller shutter outside it."""
    x0, x1, z0, z1 = WIN; y0, y1 = WALL_Y + 0.08, WALL_Y + 0.15; f = 0.055; m = (x0 + x1) / 2
    for nm, a, b, c, d in (('f_l', x0, x0 + f, z0, z1), ('f_r', x1 - f, x1, z0, z1), ('f_b', x0, x1, z0, z0 + f), ('f_t', x0, x1, z1 - f, z1), ('f_m', m - 0.045, m + 0.045, z0, z1)):
        box(nm, a, b, y0, y1, c, d, 'wframe', e=0.004, se=2)
    for k, (a, b) in enumerate(((x0 + f, m - 0.045), (m + 0.045, x1 - f))):       # the leaves
        s = 0.05
        for nm, p, q, c, d in (('l', a, a + s, z0 + f, z1 - f), ('r', b - s, b, z0 + f, z1 - f), ('b', a, b, z0 + f, z0 + f + s), ('t', a, b, z1 - f - s, z1 - f)):
            box(f'leaf{k}{nm}', p, q, y0 - 0.012, y1 - 0.01, c, d, 'wframe', e=0.004, se=2)
        box(f'glass{k}', a + 0.03, b - 0.03, y0 + 0.02, y0 + 0.024, z0 + f + 0.03, z1 - f - 0.03, 'glass')
    box('handle_a', m - 0.012, m + 0.012, y0 - 0.03, y0, (z0 + z1) / 2 - 0.02, (z0 + z1) / 2 + 0.02, 'brass', e=0.003, se=2)
    box('handle_b', m - 0.008, m + 0.008, y0 - 0.042, y0 - 0.028, (z0 + z1) / 2 - 0.12, (z0 + z1) / 2 + 0.01, 'brass', e=0.004, se=2)
    h = 0.045; z = z1 + 0.02; bottom = z0 + (z1 - z0) * shut; k = 0                # slats, from the top down to how far it is open
    while z - h >= bottom - 1e-6:
        box(f'slat{k}', x0 - 0.02, x1 + 0.02, WALL_Y + 0.18, WALL_Y + 0.192, z - h + 0.0007, z, 'slat', e=0.003, se=1); z -= h; k += 1

def build_curtains():
    """Two linen curtains, pleated, gathered at the sides of the window."""
    bm_out = []
    for nm, x0, x1, ph in (('curt_l', -0.42, -0.20, 0.3), ('curt_r', 0.98, 1.27, 1.4)):
        bm = bmesh.new(); nu, nv = 150, 12; rows = []
        for j in range(nv + 1):
            z = FLOOR_Z + 0.02 + (CEIL_Z - 0.08 - FLOOR_Z) * j / nv; row = []
            for i in range(nu + 1):
                u = i / nu; x = x0 + (x1 - x0) * u; y = WALL_Y - 0.09 + 0.026 * math.sin(u * math.pi * 9 + ph) + 0.006 * math.sin(u * 31 + z * 2)
                row.append(bm.verts.new((x, y, z)))
            rows.append(row)
        for j in range(nv):
            for i in range(nu): bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
        link(nm, bm, 'linen')

def build_stand():
    """Oak nightstand with one drawer, 460 × 380 × 500 mm, on four short legs."""
    cx, cy, w, d = 0.02, 0.03, 0.46, 0.38
    box('stand_top', cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, -0.028, 0.0, 'oak', r=0.004, e=0.0025, sp=4, se=3)
    box('stand_body', cx - w / 2 + 0.008, cx + w / 2 - 0.008, cy - d / 2 + 0.012, cy + d / 2 - 0.006, -0.40, -0.028, 'oak', r=0.002, e=0.001, sp=2, se=1)
    fy = cy - d / 2 + 0.012
    box('drawer_gap', cx - w / 2 + 0.018, cx + w / 2 - 0.018, fy - 0.001, fy, -0.225, -0.042, 'cavity')
    box('drawer', cx - w / 2 + 0.021, cx + w / 2 - 0.021, fy - 0.010, fy - 0.0005, -0.222, -0.045, 'oak', r=0.002, e=0.0015, sp=2, se=2)
    box('panel_gap', cx - w / 2 + 0.018, cx + w / 2 - 0.018, fy - 0.001, fy, -0.242, -0.2385, 'cavity')
    ob = cyl('knob', 0.011, 0.016, 'brass', (cx, fy - 0.018, -0.1335), axis='Y', seg=32)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(f'leg{sx}{sy}', 0.014, 0.10, 'oak', (cx + sx * (w / 2 - 0.05), cy + sy * (d / 2 - 0.05), -0.45), seg=24)

def build_bed(n):
    """Bed against the back wall, left of the nightstand: squared-off shapes (owner, 2026-11-08), linen and oak."""
    rbox('bed_base', 1.56, 1.96, 0.20, 0.02, 0.01, 'oak', (-1.12, -0.72, FLOOR_Z + 0.06), sp=4, se=2)
    rbox('headboard', 1.7, 0.08, 0.95, 0.03, 0.02, 'linen2', (-1.12, 0.33, FLOOR_Z), sp=6, se=3)
    rbox('mattress', 1.6, 2.0, 0.24, 0.04, 0.03, 'linen', (-1.12, -0.72, -0.24), sp=6, se=4)
    rbox('duvet', 1.66, 1.55, 0.06, 0.08, 0.03, 'linen', (-1.12, -0.95, -0.01), sp=8, se=4)
    for k, (px, ry) in enumerate(((-0.86, 0.03), (-1.50, -0.04))):       # soft pillows, clear of the arm that reaches the nightstand
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=64, radius=1.0)
        for v in bm.verts:
            x, y, z = v.co; sx = lambda a: math.copysign(abs(a) ** 0.55, a)
            q = Vector((sx(x) * 0.36, sx(y) * 0.20, z * 0.085)); w = noise.fractal(Vector((x, y, z)) * 2.2 + Vector((k * 3.1, 0, 0)), 1.0, 2.0, 3)
            v.co = q * (1 + 0.05 * w)
        ob = link(f'pillow{k}', bm, 'linen'); ob.location = (px, 0.08, BED_TOP + 0.085); ob.rotation_euler = (math.radians(10), ry * 0.5, 0)

def build_lamp(kw):
    """A table lamp on the nightstand: the smart bulb in a fabric drum (it fits a ceiling light as well)."""
    x, y, h = 0.15, 0.13, 0.31
    cyl('lamp_foot', 0.052, 0.014, 'lampmetal', (x, y, 0.007), seg=96)
    cyl('lamp_stem', 0.0055, 0.24, 'lampmetal', (x, y, 0.134), seg=32)
    bm = bmesh.new(); r0, r1, z0, z1 = 0.095, 0.08, h - 0.075, h + 0.075; n = 128; a0 = []; a1 = []
    for i in range(n):
        t = 2 * math.pi * i / n; a0.append(bm.verts.new((x + r0 * math.cos(t), y + r0 * math.sin(t), z0))); a1.append(bm.verts.new((x + r1 * math.cos(t), y + r1 * math.sin(t), z1)))
    for i in range(n): bm.faces.new((a0[i], a0[(i + 1) % n], a1[(i + 1) % n], a1[i]))
    link('lamp_shade', bm, 'shade')
    share, kelvin = kw
    if share > 0:
        L = bpy.data.lights.new('bulb', 'POINT'); L.energy = 22.0 * share; L.shadow_soft_size = 0.03; L.use_nodes = True; nt = L.node_tree
        bb = nt.nodes.new('ShaderNodeBlackbody'); bb.inputs[0].default_value = kelvin; nt.links.new(bb.outputs[0], nt.nodes['Emission'].inputs[0])
        o = bpy.data.objects.new('bulb', L); col.objects.link(o); o.location = (x, y, h)

def build_outside(n):
    """What the window really faces: ground, two apartment blocks with their windows, trees."""
    rnd = random.Random(7); Z0 = FLOOR_Z - 4.0
    box('ground', -60, 60, 1, 90, Z0 - 0.1, Z0, 'asphalt')
    for tag, x0, x1, y, floors, mat in (('a', -16, 7, 13, 6, 'facade'), ('b', 8.5, 30, 25, 8, 'facade2')):
        hh = floors * 3.1
        box(f'block{tag}', x0, x1, y, y + 12, Z0, Z0 + hh, mat)
        for fl in range(floors):
            xc = x0 + 1.7
            while xc < x1 - 1.2:
                z = Z0 + 1.0 + fl * 3.1; lit = rnd.random()
                on = (n == 1 and lit < 0.3) or (n in (4, 5) and lit < 0.05)
                box(f'w{tag}{fl}{int(xc * 10)}', xc - 0.55, xc + 0.55, y - 0.02, y + 0.02, z, z + 1.55, 'win_lit' if on else 'win_dark')
                xc += 3.3
    for name, loc, scale in (('island_tree_01', (-2.6, 9.5, Z0), 1.0), ('island_tree_02', (4.2, 12.0, Z0), 1.0)):
        before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=os.path.join(os.path.dirname(TEX), 'polyhaven', name, name + '_1k.gltf'))
        new = [o for o in bpy.data.objects if o not in before]; bpy.context.view_layer.update()
        zs = [(o.matrix_world @ Vector(c)).z for o in new if o.type == 'MESH' for c in o.bound_box]; hgt = max(zs) - min(zs); k = 11.0 / hgt * scale
        for o in new:
            if o.parent is None: o.scale = tuple(v * k for v in o.scale); o.location = loc
    if n == 1:                                             # a street lamp lights the trees and the facade from below
        L = bpy.data.lights.new('street', 'POINT'); L.energy = 900; L.color = srgb('#ffb873')[:3]; L.shadow_soft_size = 0.2
        o = bpy.data.objects.new('street', L); col.objects.link(o); o.location = (1.0, 7.0, Z0 + 5.0)

def set_sky(sky):
    w = bpy.data.worlds.new('w'); w.use_nodes = True; scene.world = w; nt = w.node_tree; bg = nt.nodes['Background']
    if sky == 'night':
        bg.inputs[0].default_value = srgb('#141c30'); bg.inputs[1].default_value = 0.08; return
    tex = nt.nodes.new('ShaderNodeTexSky'); ids = [e.identifier for e in tex.bl_rna.properties['sky_type'].enum_items]
    tex.sky_type = next(i for k in ('MULTIPLE', 'NISHITA', 'SINGLE') for i in ids if k in i)
    tex.sun_disc = False; tex.sun_elevation = math.radians(sky); tex.sun_rotation = math.radians(66)      # east-north-east: never in the window
    nt.links.new(tex.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 3.5

def wear_bracelet(R, wrist):
    """The bracelet closed on the wrist, its body against the skin on the inner side."""
    yc, zc, hw, ht = wrist_fit('palm'); br = build_bracelet(); sc = Vector(((ht + 0.0022) / STRAP_B, (hw + 0.0022) / STRAP_A, 1.0))
    B = Matrix(((0, 0, -1), (0, -1, 0), (-1, 0, 0))).to_4x4()          # columns: strap x → down, y → side, z → up the arm
    br.matrix_world = Matrix.Translation(wrist) @ R.to_4x4() @ Matrix.Translation((-0.012, yc, zc)) @ B @ Matrix.Diagonal(sc.to_4d())
    return br

def build_sleeve(R, wrist, pose='pinch', start=0.075):
    """A long sleeve from the forearm out of the frame: the arm always leaves the picture."""
    yc, zc, hw, ht = wrist_fit(pose); bm = bmesh.new(); rings = []; nr, ns = 170, 48
    for i in range(nr + 1):
        x = -start - 1.5 * i / nr; g = min(1.0, (-x - start) / 0.4); ring = []
        for j in range(ns):
            a = 2 * math.pi * j / ns; w = noise.fractal(Vector((x * 16, math.cos(a) * 1.5, math.sin(a) * 1.5)), 1.0, 2.0, 2) * 0.006
            r = 0.041 + 0.02 * g + w; ring.append(bm.verts.new(wrist + R @ Vector((x, yc + r * math.cos(a), zc + r * math.sin(a) * 0.92))))
        rings.append(ring)
    for i in range(nr):
        A, B = rings[i], rings[i + 1]
        for j in range(ns): bm.faces.new((A[j], A[(j + 1) % ns], B[(j + 1) % ns], B[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return link('sleeve', bm, 'cotton')

def build_arm(n):
    if n == 1:                                             # 22:00: the hand lifts the bracelet off the base; the arm comes in from the left, in a sleeve
        F = Vector((1, 0.12, -0.30)).normalized(); R = basis(F, Vector((0, 0.3, 1)))       # sitting on the bed (owner, 2026-11-09): the forearm almost level, not coming down from above
        wr = Vector((-0.11, -0.05, 0.17)); hand, tips = build_hand('pinch', R, wr); build_sleeve(R, wr)
        mid = (tips['index'] + tips['thumb']) / 2; d = Vector((0.78, -0.30, -0.55)).normalized(); xv = -d   # the ring hangs from the pinch, towards the camera
        cam = Vector((0.85, -1.30, 0.65)).normalized(); cp = (cam - xv * cam.dot(xv)).normalized(); side = xv.cross(cp)
        zv = (cp * 0.62 + side * 0.78).normalized(); yv = zv.cross(xv)                                     # tilted: the woven band shows, not just its edge
        Rb = Matrix((xv, yv, zv)).transposed(); br = build_bracelet()
        br.matrix_world = Matrix.Translation(mid + d * 0.020 - Rb @ Vector((STRAP_XF, 0, STRAP_LIFT + STRAP_H / 2))) @ Rb.to_4x4()   # beyond the fingertips: the fist would hide it
    elif n == 5:                                           # 06:20: from under the duvet, the palm on the base, the bracelet on the wrist
        F = Vector((1, 0.36, 0.03)).normalized(); R = basis(F, Vector((0, 0, 1)).cross(F))
        L_ = Vector(HAND_TIPS['palm']['index']).x; wrist = Vector((0.05 - L_, -0.01, TOP - palm_z('palm')))
        hand, _ = build_hand('palm', R, wrist); wrist.z += rest_on_top(hand); wear_bracelet(R, wrist); build_sleeve(R, wrist, 'palm', 0.12)
    else:                                                  # asleep: the forearm out of the covers on the duvet, the bracelet on the wrist
        F = Vector((1, 0.30, 0.17)).normalized(); Y = Vector((0, 0, 1)).cross(F); roll = math.radians(RELAX_ROLL)      # soft, a little on its side, lying on the sheet inside the bed's edge (owner, 2026-11-09)
        R = basis(F, Y * math.cos(roll) + Vector((0, 0, 1)) * math.sin(roll)); vs, _ = hand_mesh('relax')
        low = min((R @ Vector(v)).z for v in vs if v[0] > -0.01); wrist = Vector((RELAX_X, RELAX_Y, -0.006 - low))
        build_hand('relax', R, wrist); wear_bracelet(R, wrist); build_sleeve(R, wrist, 'palm', 0.12)

def bedroom_scene(n):
    t, lamp, ring, shut, expo, sky = ROOM[n]
    mat_room()
    # the light strip is the only source of the halo (owner, 2026-11-08: real light, no glow painted on the wood): it leaves the 2 mm gap at a grazing angle, so it tints the wood and fades fast
    MATS['led_under'] = emit('led_under', srgb(ring), LED_W[n]) if ring else principled('led_under', srgb('#141416'), rough=0.6)
    MATS['dots'] = emit('dots', srgb('#ffd9a0'), 2.5 if n == 3 else 6.0)
    b_ = build_base(with_time=bool(t), time=t or '06:30'); b_.rotation_euler = (0, 0, BASE_ROT)
    build_shell(); build_window(shut); build_curtains(); build_stand(); build_bed(n); build_lamp(lamp)
    if shut > 0: build_outside(n)
    if ring: only_on_the_wood(bpy.data.objects['ring'], *led_spill(srgb(ring), LED_SPILL[n]))
    build_arm(n)
    set_sky(sky)
    x0, x1, z0, z1 = WIN
    if shut > 0:                                           # the window as a portal: the sky's light is sampled through it
        zt = z0 + (z1 - z0) * shut
        ld = bpy.data.lights.new('portal', 'AREA'); ld.shape = 'RECTANGLE'; ld.size = x1 - x0; ld.size_y = zt - z0; ld.cycles.is_portal = True
        o = bpy.data.objects.new('portal', ld); col.objects.link(o); o.location = ((x0 + x1) / 2, WALL_Y + 0.17, (z0 + zt) / 2); o.rotation_euler = (math.pi / 2, 0, 0)
    else:                                                  # shutters closed: only what the eye finds in the dark
        area('dark', (-0.4, -1.4, 1.8), (0, 0, 0), 2.5, 1.8, (0.50, 0.60, 1.0))
    look((0.46, -1.48, 0.78), (-0.02, 0.06, 0.03), 55, 4.0)
    scene.view_settings.exposure = expo
