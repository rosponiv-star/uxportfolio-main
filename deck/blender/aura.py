# AuraWake objects for the Polimi deck (owner, 2026-10-27).
# One model, two outputs:
#   blender -b -P deck/blender/aura.py -- real <outdir> <shot> [preview]   shot = hero | night | dawn
#   blender -b -P deck/blender/aura.py -- line <outdir>                      isometric technical drawings + anchors.json
# Base: rounded square block of black anodised aluminium (Mac mini proportions, Teenage Engineering restraint), only a
# power cable at the back, one small LED at the front, the time behind micro-perforations (lit only when needed), a
# shallow cradle on top for the bracelet pod, a light line underneath that washes the nightstand.
import bpy, bmesh, math, json, sys, os
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index('--') + 1:]
MODE, OUT = argv[0], os.path.abspath(argv[1])
SHOT = argv[2] if len(argv) > 2 else ''
PREVIEW = 'preview' in argv
PLASTIC = 'plastic' in argv
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = scene.collection

# ---------------------------------------------------------------------------------------------------------------
# Dimensions (metres)
W, H, PL, ST = 0.12, 0.0428, 0.0022, 0.0   # width/depth, body height, plinth height, light strip
TOP = PL + ST + H                               # top surface
MID = PL + ST + H / 2                           # middle of the front and back faces
FONT_PATH = 'C:/Windows/Fonts/segoeuisl.ttf'
NIGHT, DAWN = '#7a86e8', '#f2c074'

def srgb(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)

def grey(v):
    return srgb('#%02x%02x%02x' % ((round(v * 255),) * 3))

# ---------------------------------------------------------------------------------------------------------------
# Materials: one name per role; built differently for the realistic and the line mode.
MATS = {}

def principled(name, color, metal=0.0, rough=0.5, coat=0.0, aniso=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = color
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    for k, v in (('Coat Weight', coat), ('Clearcoat', coat), ('Anisotropic', aniso)):
        if k in b.inputs: b.inputs[k].default_value = v
    return m

def emit(name, color, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); o = nt.nodes.new('ShaderNodeOutputMaterial')
    e.inputs['Color'].default_value = color; e.inputs['Strength'].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0])
    return m

def toon(name, color):
    """Flat fill for the technical drawings: three tones from the face normal (top light, sides darker)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    g = nt.nodes.new('ShaderNodeNewGeometry')
    d = nt.nodes.new('ShaderNodeVectorMath'); d.operation = 'DOT_PRODUCT'
    d.inputs[1].default_value = Vector((0.25, -0.45, 0.86)).normalized()
    r = nt.nodes.new('ShaderNodeValToRGB'); r.color_ramp.interpolation = 'CONSTANT'
    els = r.color_ramp.elements
    els[0].position, els[0].color = 0.0, (0.80, 0.80, 0.80, 1)
    els[1].position, els[1].color = 0.62, (1, 1, 1, 1)
    mid = els.new(0.25); mid.color = (0.90, 0.90, 0.90, 1)
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0
    mul.inputs[6].default_value = color
    e = nt.nodes.new('ShaderNodeEmission'); o = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(g.outputs['Normal'], d.inputs[0])
    nt.links.new(d.outputs['Value'], r.inputs['Fac'])
    nt.links.new(r.outputs['Color'], mul.inputs[7])
    nt.links.new(mul.outputs[2], e.inputs['Color'])
    nt.links.new(e.outputs[0], o.inputs[0])
    return m

def wood():
    m = bpy.data.materials.new('wood'); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 14.0, 1.0)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 8
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 6.0; wv.inputs['Distortion'].default_value = 6.0
    wv.inputs['Detail'].default_value = 4
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = srgb('#2a170c'); ramp.color_ramp.elements[1].color = srgb('#5a3820')
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
    nt.links.new(wv.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.42
    return m

def grille(name, dark, slit):
    """Plinth = speaker grille: vertical slits on the sides, a ring of radial slits on the bottom (Mac mini language)."""
    m = principled(name, dark, rough=0.88); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); g = nt.nodes.new('ShaderNodeNewGeometry')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs[0])
    def op(o, a, b=None, v=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = o
        for i, x in enumerate((a, b)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    ang = op('ARCTAN2', sep.outputs[1], sep.outputs[0])
    stripe = op('GREATER_THAN', op('SINE', op('MULTIPLY', ang, 220.0)), 0.35)
    rad = op('SQRT', op('ADD', op('POWER', sep.outputs[0], 2.0), op('POWER', sep.outputs[1], 2.0)))
    sn = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(g.outputs['Normal'], sn.inputs[0])
    side = op('LESS_THAN', op('ABSOLUTE', sn.outputs[2]), 0.5)
    ring = op('MULTIPLY', op('MULTIPLY', op('LESS_THAN', sn.outputs[2], -0.5), op('GREATER_THAN', rad, 0.0335)), op('LESS_THAN', rad, 0.0405))
    zdots = op('GREATER_THAN', op('SINE', op('MULTIPLY', sep.outputs[2], 2600.0)), 0.35)
    mask = op('MAXIMUM', op('MULTIPLY', op('MULTIPLY', stripe, zdots), side), op('MULTIPLY', stripe, ring))
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs[6].default_value = dark; mix.inputs[7].default_value = slit
    nt.links.new(mask, mix.inputs['Factor']); nt.links.new(mix.outputs[2], b.inputs['Base Color'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.6; bump.inputs['Distance'].default_value = 0.0004
    nt.links.new(op('SUBTRACT', 1.0, mask), bump.inputs['Height']); nt.links.new(bump.outputs[0], b.inputs['Normal'])
    return m

def bump_tex(m, kind, scale, strength, dist=0.0002, vec=None):
    """Micro texture: bead-blasted noise or fine diagonal ribs (band, braided cable)."""
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; tc = nt.nodes.new('ShaderNodeTexCoord')
    if kind == 'noise':
        t = nt.nodes.new('ShaderNodeTexNoise'); t.inputs['Scale'].default_value = scale; t.inputs['Detail'].default_value = 2
    else:
        t = nt.nodes.new('ShaderNodeTexWave'); t.wave_type = 'BANDS'; t.bands_direction = 'DIAGONAL'
        t.inputs['Scale'].default_value = scale
    nt.links.new(tc.outputs['Object'], t.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = strength; bp.inputs['Distance'].default_value = dist
    nt.links.new(t.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs[0], b.inputs['Normal'])
    return m

HOLE_D = 0.0013
EDGE_P, EDGE_T = 0.0012, 0.0006   # corner and top/bottom edge radii: the grid sits on the flat part of each face

def grid(L, n, d=HOLE_D):
    """n holes on a flat length L: the gap between holes equals the gap to the edge. Returns (pitch, offset, n)."""
    g = (L - n * d) / (n + 1)
    return d + g, (0.0 if n % 2 else (d + g) / 2), n

PU, OU, NU = grid(W - 2 * EDGE_P, 29)   # small holes, wide gaps (owner ref): gap ≈ 2.66 mm
PV, OV, NV = grid(H - 2 * EDGE_T, 10)   # gap ≈ 2.60 mm
def cols(p, o, n): return [-(n - 1) / 2 * p + i * p for i in range(n)]
R_TOP, R_BOT = 0.0004, 0.0009   # hole radius, top row → bottom row (owner: graded, small at the top)
SPAN_V = (NV - 1) / 2 * PV
def hole_r(cv): return R_BOT + (R_TOP - R_BOT) * (cv + SPAN_V) / (2 * SPAN_V)
BTN_CLEAR = 0.0085  # clears the button's gap plus the 2 + 2 holes beside it
BTN_X = -9 * PU            # Bluetooth button on a hole column, right of the inlet seen from behind (world -X)

def speaker_mask(nt):
    """Speaker holes on the sides and the back; around the inlet and the button whole holes are left out, so both sit
    centred in the gap."""
    tc = nt.nodes.new('ShaderNodeTexCoord'); g = nt.nodes.new('ShaderNodeNewGeometry')
    P = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], P.inputs[0])
    Nn = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(g.outputs['Normal'], Nn.inputs[0])
    def op(o, a, b=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = o
        for i, x in enumerate((a, b)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    x, y, z = P.outputs[0], P.outputs[1], P.outputs[2]
    isX = op('GREATER_THAN', op('ABSOLUTE', Nn.outputs[0]), 0.5)
    isB = op('GREATER_THAN', Nn.outputs[1], 0.5)
    u = op('ADD', op('MULTIPLY', isX, y), op('MULTIPLY', isB, x))
    v = op('SUBTRACT', z, MID)
    iu, iv = op('ROUND', op('DIVIDE', op('SUBTRACT', u, OU), PU)), op('ROUND', op('DIVIDE', op('SUBTRACT', v, OV), PV))
    cu, cv = op('ADD', op('MULTIPLY', iu, PU), OU), op('ADD', op('MULTIPLY', iv, PV), OV)
    fu, fv = op('SUBTRACT', u, cu), op('SUBTRACT', v, cv)
    rr = op('ADD', R_BOT, op('MULTIPLY', op('DIVIDE', op('ADD', cv, SPAN_V), 2 * SPAN_V), R_TOP - R_BOT))
    hole = op('LESS_THAN', op('ADD', op('MULTIPLY', fu, fu), op('MULTIPLY', fv, fv)), op('MULTIPLY', rr, rr))
    region = op('MULTIPLY', op('LESS_THAN', op('ABSOLUTE', cu), (NU - 1) / 2 * PU + 1e-5), op('LESS_THAN', op('ABSOLUTE', cv), (NV - 1) / 2 * PV + 1e-5))
    def away(cx, rr):  # whole holes only: distance from the hole centre
        return op('GREATER_THAN', op('ADD', op('POWER', op('SUBTRACT', cu, cx), 2.0), op('POWER', cv, 2.0)), rr * rr)
    back = op('MULTIPLY', isB, op('MULTIPLY', away(0.0, 0.0066), away(BTN_X, BTN_CLEAR)))
    return op('MULTIPLY', op('MULTIPLY', hole, region), op('MAXIMUM', isX, back))

def satin(name, color):
    m = principled(name, color, metal=0.0 if PLASTIC else 1.0, rough=0.8 if PLASTIC else 0.38); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 1, 1)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6500.0 if PLASTIC else 9000.0; nz.inputs['Detail'].default_value = 2
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.3 if PLASTIC else 0.05; bp.inputs['Distance'].default_value = 0.0001
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs[0], b.inputs['Normal'])
    return m

def body_real(name, color):
    m = satin(name, color)
    return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; mk = speaker_mask(nt)
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs[6].default_value = color; mix.inputs[7].default_value = (0.005, 0.005, 0.006, 1)
    nt.links.new(mk, mix.inputs['Factor']); nt.links.new(mix.outputs[2], b.inputs['Base Color'])
    mr = nt.nodes.new('ShaderNodeMath'); mr.operation = 'SUBTRACT'; mr.inputs[0].default_value = 1.0
    nt.links.new(mk, mr.inputs[1]); nt.links.new(mr.outputs[0], b.inputs['Metallic'])
    return m

def body_toon(name, color):
    m = toon(name, color); nt = m.node_tree; mk = speaker_mask(nt)
    e = next(n for n in nt.nodes if n.type == 'EMISSION'); src = e.inputs['Color'].links[0].from_socket
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[7].default_value = grey(0.32)
    nt.links.new(src, mix.inputs[6]); nt.links.new(mk, mix.inputs['Factor']); nt.links.new(mix.outputs[2], e.inputs['Color'])
    return m

def fabric(name, color):
    m = principled(name, color, rough=0.92); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    for k, v in (('Sheen Weight', 0.25), ('Sheen', 0.25)):
        if k in b.inputs: b.inputs[k].default_value = v; break
    tc = nt.nodes.new('ShaderNodeTexCoord'); P = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], P.inputs[0])
    def op(o, a, c=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = o
        for i, x in enumerate((a, c)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    weave = op('MULTIPLY', op('SINE', op('MULTIPLY', P.outputs[0], 5200.0)), op('SINE', op('MULTIPLY', P.outputs[1], 5200.0)))
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.45; bp.inputs['Distance'].default_value = 0.00015
    nt.links.new(weave, bp.inputs['Height']); nt.links.new(bp.outputs[0], b.inputs['Normal'])
    return m

def loop_fabric(name, dark, light, edge, R=0.031, h=0.020, lift=0.0018, p=0.00042):
    """Woven strap, thread by thread: a 2/1 twill (diagonal), warp threads graphite, weft threads melange light grey,
    each thread rounded in the bump, fibre fuzz, the two edges woven in orange. Coordinates: u along the strap
    (angle x R), v across it (z)."""
    m = principled(name, dark, rough=0.9); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    for k in ('Sheen Weight', 'Sheen'):
        if k in b.inputs: b.inputs[k].default_value = 0.45; break
    if 'Sheen Roughness' in b.inputs: b.inputs['Sheen Roughness'].default_value = 0.35
    tc = nt.nodes.new('ShaderNodeTexCoord'); P = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], P.inputs[0])
    def op(o, a, c=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = o
        for i, x in enumerate((a, c)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    u = op('MULTIPLY', op('ARCTAN2', P.outputs[1], P.outputs[0]), R)
    v = P.outputs[2]
    fu, fv = op('DIVIDE', u, p), op('DIVIDE', v, p)
    iu, iv = op('FLOOR', fu), op('FLOOR', fv)
    tw = op('FLOORED_MODULO', op('SUBTRACT', iu, iv), 3.0)
    weft = op('LESS_THAN', tw, 0.5)                       # weft on top in one cell of three, shifted each row: twill
    ru = op('SINE', op('MULTIPLY', op('FRACT', fu), math.pi))   # thread section, rounded
    rv = op('SINE', op('MULTIPLY', op('FRACT', fv), math.pi))
    height = op('ADD', op('MULTIPLY', weft, rv), op('MULTIPLY', op('SUBTRACT', 1.0, weft), ru))
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 9000.0; nz.inputs['Detail'].default_value = 6
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    h2 = op('ADD', op('POWER', height, 0.6), op('MULTIPLY', nz.outputs['Fac'], 0.25))
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.85; bp.inputs['Distance'].default_value = 0.00025
    nt.links.new(h2, bp.inputs['Height']); nt.links.new(bp.outputs[0], b.inputs['Normal'])
    # colour: melange weft (light grey with fibre variation) over graphite warp; orange threads on both edges
    mel = nt.nodes.new('ShaderNodeMix'); mel.data_type = 'RGBA'; mel.inputs[6].default_value = light
    mel.inputs[7].default_value = tuple(c * 0.55 for c in light[:3]) + (1,)
    cell = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(iu, cell.inputs[0]); nt.links.new(iv, cell.inputs[1])
    vn = nt.nodes.new('ShaderNodeTexWhiteNoise'); vn.noise_dimensions = '3D'; nt.links.new(cell.outputs[0], vn.inputs['Vector'])
    nt.links.new(op('ADD', op('MULTIPLY', vn.outputs['Value'], 0.7), op('MULTIPLY', nz.outputs['Fac'], 0.3)), mel.inputs['Factor'])
    col_ = nt.nodes.new('ShaderNodeMix'); col_.data_type = 'RGBA'; col_.inputs[6].default_value = dark
    nt.links.new(op('MULTIPLY', weft, 0.85), col_.inputs['Factor']); nt.links.new(mel.outputs[2], col_.inputs[7])
    edge_m = op('MAXIMUM', op('LESS_THAN', v, lift + 0.0015), op('GREATER_THAN', v, lift + h - 0.0015))
    fin = nt.nodes.new('ShaderNodeMix'); fin.data_type = 'RGBA'; fin.inputs[7].default_value = edge
    nt.links.new(col_.outputs[2], fin.inputs[6]); nt.links.new(edge_m, fin.inputs['Factor'])
    shade_ = nt.nodes.new('ShaderNodeMix'); shade_.data_type = 'RGBA'; shade_.blend_type = 'MULTIPLY'; shade_.inputs['Factor'].default_value = 1.0
    nt.links.new(fin.outputs[2], shade_.inputs[6])
    sh = nt.nodes.new('ShaderNodeCombineColor'); g = op('ADD', 0.7, op('MULTIPLY', height, 0.3))
    for k in range(3): nt.links.new(g, sh.inputs[k])
    nt.links.new(sh.outputs[0], shade_.inputs[7]); nt.links.new(shade_.outputs[2], b.inputs['Base Color'])
    return m

TABLE = SHOT == 'table'
STUDIO = SHOT in ('foot', 'persp_band', 'table', 'front', 'back', 'top', 'bottom', 'cable', 'persp', 'lit', 'band', 'persp_back')
if MODE == 'real':
    MATS = {
        'body': body_real('body', srgb('#2c2d31')),
        'shell': satin('shell', srgb('#2c2d31')),
        'alu': bump_tex(principled('alu', srgb('#18181b'), metal=1.0, rough=0.5), 'noise', 4000, 0.04),
        'grille': grille('grille', srgb('#060607'), srgb('#000000')),
        'rubber': principled('rubber', srgb('#0a0a0b'), rough=0.8),
        'cavity': principled('cavity', srgb('#050506'), rough=0.9),
        'print': principled('print', srgb('#7a7a7e'), rough=0.6),
        'pin': principled('pin', srgb('#c8c8cc'), metal=1.0, rough=0.25),
        'led_under': principled('led_under', srgb('#141416'), rough=0.6) if STUDIO and SHOT != 'lit' else
                     emit('led_under', srgb(NIGHT if SHOT == 'night' else DAWN), 90.0 if SHOT == 'night' else 160.0 if SHOT == 'lit' else 70.0),
        'led_front': emit('led_front', srgb('#ffffff'), 3.0 if STUDIO else 0.0),
        'dots': emit('dots', srgb('#ffd9a0'), 7.0),
        'band': principled('band', srgb('#2a2b2f'), rough=0.62),
        'fabric': fabric('fabric', srgb('#1c1d20')),
        'loop': loop_fabric('loop', srgb('#2a2b2f'), srgb('#76746f'), srgb('#d9592a')),
        'modalu': bump_tex(principled('modalu', srgb('#2c2d31'), metal=1.0, rough=0.38), 'noise', 9000, 0.05),
        'cable': bump_tex(principled('cable', srgb('#0e0e10'), rough=0.8), 'wave', 420, 0.5),
        'plug': principled('plug', srgb('#0a0a0b'), rough=0.6),
    }
else:
    T = {'alu': 0.86, 'grille': 0.42, 'rubber': 0.3, 'print': 0.4, 'pin': 0.75, 'band': 0.5, 'cable': 0.25, 'dots': 0.28,
         'led_front': 0.25, 'phone': 0.88, 'screen': 0.30, 'ui': 0.92, 'card': 0.5, 'metal': 0.74, 'glass': 0.98,
         'frame': 0.96, 'fabric': 0.5, 'loop': 0.5, 'modalu': 0.4, 'slat': 0.80, 'pane': 0.90, 'cap': 0.70, 'plug': 0.3}
    MATS = {k: toon(k, grey(v)) for k, v in T.items()}
    MATS['body'] = body_toon('body', grey(0.86))
    MATS['shell'] = toon('shell', grey(0.86))
    MATS['led_under'] = toon('led_under', srgb(DAWN))

def M(name):
    return MATS.get(name) or MATS.setdefault(name, principled(name, grey(0.5)))

# ---------------------------------------------------------------------------------------------------------------
# Geometry helpers
def link(name, bm, mat, loc=(0, 0, 0), smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); col.objects.link(ob)
    ob.location = loc; me.materials.append(M(mat))
    if smooth: shade(ob)
    return ob

def shade(ob, angle=32):
    me = ob.data
    for p in me.polygons: p.use_smooth = True
    try: me.set_sharp_from_angle(angle=math.radians(angle))
    except AttributeError:
        me.use_auto_smooth = True; me.auto_smooth_angle = math.radians(angle)

def rbox_bm(w, d, h, rp, re, sp=16, se=4):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * w, v.co.y * d, v.co.z * h + h / 2))
    if rp > 0:
        ve = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > 1e-7]
        bmesh.ops.bevel(bm, geom=ve, offset=rp, segments=sp, profile=0.5, affect='EDGES', clamp_overlap=True)
    if re > 0:
        he = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) < 1e-7]
        bmesh.ops.bevel(bm, geom=he, offset=re, segments=se, profile=0.5, affect='EDGES', clamp_overlap=True)
    return bm

def rbox(name, w, d, h, rp, re, mat, loc=(0, 0, 0), sp=16, se=4):
    return link(name, rbox_bm(w, d, h, rp, re, sp, se), mat, loc)

def cyl(name, r, h, mat, loc, axis='Z', seg=48):
    bm = bmesh.new()
    rot = {'Z': Matrix(), 'Y': Matrix.Rotation(math.pi / 2, 4, 'X'), 'X': Matrix.Rotation(math.pi / 2, 4, 'Y')}[axis]
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h, matrix=rot)
    return link(name, bm, mat, loc)

def ring_bm(R, w, t, n=128):
    """Band loop in the YZ plane: rectangular section, width w along X, thickness t radial."""
    bm = bmesh.new(); rings = []
    for i in range(n):
        a = 2 * math.pi * i / n; c, s = math.cos(a), math.sin(a)
        rings.append([bm.verts.new((x, (R + rr) * c, (R + rr) * s)) for x, rr in ((-w / 2, -t / 2), (w / 2, -t / 2), (w / 2, t / 2), (-w / 2, t / 2))])
    for i in range(n):
        a, b = rings[i], rings[(i + 1) % n]
        for k in range(4): bm.faces.new((a[k], a[(k + 1) % 4], b[(k + 1) % 4], b[k]))
    return bm

def boolean_diff(ob, cutter):
    mod = ob.modifiers.new('cut', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cutter
    if hasattr(mod, 'solver'): mod.solver = 'EXACT'
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.remove(mod); old = ob.data; ob.data = me; bpy.data.meshes.remove(old)
    bpy.data.objects.remove(cutter); shade(ob)
    wn = ob.modifiers.new('wn', 'WEIGHTED_NORMAL'); wn.keep_sharp = True; wn.mode = 'FACE_AREA'

def curve(name, pts, r, mat):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu); col.objects.link(ob); cu.materials.append(M(mat))
    return ob

def group(name, obs, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); col.objects.link(e); e.location = loc
    for o in obs: o.parent = e
    return e

# 5×7 dot-matrix digits for the time behind the micro-perforation
FONT = {'0': ['01110', '10001', '10011', '10101', '11001', '10001', '01110'],
        '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
        '3': ['11111', '00010', '00100', '00010', '00001', '10001', '01110'],
        '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
        '6': ['00110', '01000', '10000', '11110', '10001', '10001', '01110'],
        ':': ['0', '0', '1', '0', '1', '0', '0']}

def time_dots(text, zc, pitch=0.0017, r=0.0005, xo=-0.006):
    cols = []
    for i, ch in enumerate(text):
        if i: cols.append(None)
        g = FONT[ch]
        for c in range(len(g[0])): cols.append([g[row][c] == '1' for row in range(7)])
    x0 = xo - (len(cols) - 1) * pitch / 2
    bm = bmesh.new()
    for ci, c in enumerate(cols):
        if c is None: continue
        for row, on in enumerate(c):
            if on:
                m = Matrix.Translation((x0 + ci * pitch, -W / 2 - 0.00005, zc + (3 - row) * pitch)) @ Matrix.Rotation(math.pi / 2, 4, 'X')
                bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=r, depth=0.0003, matrix=m)
    return link('time', bm, 'dots', smooth=False)

# ---------------------------------------------------------------------------------------------------------------
# Objects
def label(text, size, loc, rot, mat='print'):
    cu = bpy.data.curves.new('t', 'FONT'); cu.body = text; cu.font = bpy.data.fonts.load(FONT_PATH, check_existing=True)
    cu.size = size; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.extrude = 0.00002
    ob = bpy.data.objects.new('t', cu); col.objects.link(ob); ob.location = loc; ob.rotation_euler = rot
    cu.materials.append(M(mat)); return ob

def cutter_bm(shapes, depth):
    """Union of cylinders along Y (x, z, r) as one cutter mesh."""
    bm = bmesh.new()
    for x, z, r in shapes:
        m = Matrix.Translation((x, 0, z)) @ Matrix.Rotation(math.pi / 2, 4, 'X')
        bmesh.ops.create_cone(bm, cap_ends=True, segments=64, radius1=r, radius2=r, depth=depth, matrix=m)
    return bm

def stadium_bm(w, h, depth, seg=16):
    """One clean manifold prism with a stadium section in the XZ plane (USB-C opening), along Y."""
    r = h / 2; pts = []
    for cx, a0 in ((w / 2 - r, -90), (-(w / 2 - r), 90)):
        for k in range(seg + 1):
            a = math.radians(a0 + 180 * k / seg); pts.append((cx + r * math.cos(a), r * math.sin(a)))
    bm = bmesh.new(); vs = [bm.verts.new((x, -depth / 2, z)) for x, z in pts]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=(0, depth, 0), verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm

def holes_bm(depth=0.0032, seg=16):
    """Every speaker hole as its own cylinder (no overlaps), graded top → bottom: sides along X, back along Y, the inlet
    and button gaps left out."""
    bm = bmesh.new()
    def add(m, r):
        bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=depth, matrix=m)
    for u in cols(PU, OU, NU):
        for cv in cols(PV, OV, NV):
            z, r = MID + cv, hole_r(cv)
            for sx in (-1, 1):
                add(Matrix.Translation((sx * W / 2, u, z)) @ Matrix.Rotation(math.pi / 2, 4, 'Y'), r)
            if u * u + cv * cv > 0.0066 ** 2 and (u - BTN_X) ** 2 + cv * cv > BTN_CLEAR ** 2:
                add(Matrix.Translation((u, W / 2, z)) @ Matrix.Rotation(math.pi / 2, 4, 'X'), r)
    return bm

def cut(ob, bm, loc, mat):
    me = bpy.data.meshes.new('c'); bm.to_mesh(me); bm.free(); me.materials.append(M(mat))
    c = bpy.data.objects.new('c', me); col.objects.link(c); c.location = loc
    mod = ob.modifiers.new('cut', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = c
    if hasattr(mod, 'solver'): mod.solver = 'EXACT'
    if hasattr(mod, 'material_mode'): mod.material_mode = 'TRANSFER'
    dg = bpy.context.evaluated_depsgraph_get(); new = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.remove(mod); old = ob.data; ob.data = new; bpy.data.meshes.remove(old); bpy.data.objects.remove(c)
    shade(ob)

def build_base(with_time=False, time='06:14'):
    """Solid graphite block: speakers behind dot grilles on the sides and back, time + LED at the front, USB-C and the
    Bluetooth button at the back, haptic + magnetic top for the bracelet, thin rubber disc ringed by the light strip."""
    body = rbox('body', W, W, H, EDGE_P, EDGE_T, 'body', (0, 0, PL), sp=4, se=2)
    cut(body, stadium_bm(0.0084, 0.0026, 0.012), (0, W / 2, MID), 'rubber')  # USB-C receptacle
    cut(body, cutter_bm([(BTN_X, 0, 0.0057)], 0.002), (0, W / 2, MID), 'rubber')
    if MODE == 'real': cut(body, holes_bm(), (0, 0, 0), 'cavity')
    wn = body.modifiers.new('wn', 'WEIGHTED_NORMAL'); wn.keep_sharp = True; wn.mode = 'FACE_AREA'
    btn = cyl('button', 0.0049, 0.002, 'shell', (BTN_X, W / 2 - 0.0008, MID), axis='Y')
    tongue = rbox('tongue', 0.0066, 0.004, 0.0007, 0.0003, 0.0, 'print', (0, W / 2 - 0.0035, MID - 0.00035), sp=4)
    disc = cyl('disc', 0.034, PL, 'rubber', (0, 0, PL / 2), seg=128)
    ring = cyl('ring', 0.0343, PL * 0.5, 'led_under', (0, 0, PL / 2), seg=128)
    dot = cyl('led_front', 0.00085, 0.0003, 'led_front', (0.036, -W / 2 - 0.00002, MID), axis='Y', seg=24)
    obs = [body, btn, tongue, disc, ring, dot]
    if with_time: obs.append(time_dots(time, MID))
    return group('base', obs)

def band_profile(w=0.0195, t=0.0034):
    cu = bpy.data.curves.new('prof', 'CURVE'); cu.dimensions = '2D'
    sp = cu.splines.new('POLY'); r = t / 2; pts = []
    for cx, a0 in ((w / 2 - r, -90), (-(w / 2 - r), 90)):
        for k in range(9):
            a = math.radians(a0 + 180 * k / 8); pts.append((cx + r * math.cos(a), r * math.sin(a)))
    sp.points.add(len(pts) - 1); sp.use_cyclic_u = True
    for pt, (x, y) in zip(sp.points, pts): pt.co = (x, y, 0, 1)
    ob = bpy.data.objects.new('prof', cu); col.objects.link(ob); ob.hide_render = True
    return ob

def sweep(name, pts, mat, cyclic=False):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_mode = 'OBJECT'
    cu.bevel_object = band_profile(); cu.use_fill_caps = True; cu.resolution_u = 24; cu.twist_mode = 'MINIMUM'
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1); sp.use_cyclic_u = cyclic; sp.use_smooth = True
    for bp, p in zip(sp.bezier_points, pts): bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu); col.objects.link(ob); cu.materials.append(M(mat))
    return ob

def build_bracelet_open():
    """Unbuckled band lying on top of the base, sensor side down, straps over the front and back edges."""
    t, z = 0.0034, TOP + 0.0017
    e = W / 2
    pts = [(0, -e - 0.0016, TOP - 0.03), (0, -e - 0.0019, TOP - 0.008), (0, -e + 0.0035, z), (0, 0, z),
           (0, e - 0.0035, z), (0, e + 0.0019, TOP - 0.008), (0, e + 0.0016, TOP - 0.034)]
    band = sweep('band', pts, 'band')
    pod = rbox('pod', 0.0198, 0.036, 0.0024, 0.006, 0.0011, 'band', (0, 0, TOP + t - 0.0004), sp=12, se=3)
    return group('bracelet', [band, pod])

def frame(name, sx, sy, sz, bar, mat, loc):
    """Rectangular ring around the strap (buckle, keeper)."""
    x, y, z = loc
    return [rbox(f'{name}{i}', w, d, sz, 0.0, 0.0004, mat, (x + dx, y + dy, z), sp=1, se=2) for i, (w, d, dx, dy) in enumerate((
        (sx, bar, 0, -(sy - bar) / 2), (sx, bar, 0, (sy - bar) / 2), (bar, sy, -(sx - bar) / 2, 0), (bar, sy, (sx - bar) / 2, 0)))]

def strap_ring(name, R, h, t, z, flat=None, arc=None, n=240, cr=0.0009):
    """Strap as a ring with the axis vertical (lying on its edge). flat=(angle, D) flattens it against the pod;
    arc=(a0, a1) makes an open segment (the overlapping tail)."""
    bm = bmesh.new(); rings = []
    a0, a1 = arc if arc else (0.0, 2 * math.pi)
    m = n if not arc else max(8, int(n * (a1 - a0) / (2 * math.pi)))
    for i in range(m + (1 if arc else 0)):
        a = a0 + (a1 - a0) * i / m
        r = R
        if flat:
            c = math.cos(a - flat[0])
            if c > 1e-3: r = min(R, flat[1] / c)
        pts = []
        for (cx, cz, q0) in ((r - cr, z + h - cr, 0), (r - t + cr, z + h - cr, 90), (r - t + cr, z + cr, 180), (r - cr, z + cr, 270)):
            for k in range(4):
                q = math.radians(q0 + 90 * k / 3); pts.append((cx + cr * math.cos(q), cz + cr * math.sin(q)))
        rings.append([bm.verts.new((rr * math.cos(a), rr * math.sin(a), zz)) for rr, zz in pts])
    k = len(rings[0])
    for i in range(len(rings) - (1 if arc else 0)):
        A, B = rings[i], rings[(i + 1) % len(rings)]
        for q in range(k): bm.faces.new((A[q], A[(q + 1) % k], B[(q + 1) % k], B[q]))
    if arc:
        for ring in (rings[0], rings[-1]): bm.faces.new(ring if ring is rings[-1] else list(reversed(ring)))
    return link(name, bm, 'loop')

def foot_bm(R, t, a0, a1, hgt, flare, spread=0.045, n=48):
    """Charging foot under the strap's lower edge: flush with the inside (nothing touches the wrist), widening slightly
    outward and along the strap as it goes down, to a flat contact face."""
    bm = bmesh.new(); rings = []
    for i in range(n + 1):
        k = i / n; at = a0 + (a1 - a0) * k; ab = a0 - spread + (a1 - a0 + 2 * spread) * k
        P = lambda a, r, z: bm.verts.new((r * math.cos(a), r * math.sin(a), z))
        rings.append([P(at, R - t, hgt), P(at, R, hgt), P(ab, R + flare, 0.0), P(ab, R - t, 0.0)])
    for i in range(n):
        A, B = rings[i], rings[i + 1]
        for q in range(4): bm.faces.new((A[q], A[(q + 1) % 4], B[(q + 1) % 4], B[q]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm

def build_bracelet(z0=0.0, R=0.031, h=0.020, t=0.0034, lift=0.0018):
    """Woven loop strap (owner refs: Sport Loop), graphite melange with orange edges, closed, resting on its edge. The
    sensor pod is woven into the strap (no bump inside); only its charging foot shows, under the lower edge."""
    ap = math.radians(-60)
    parts = [strap_ring('strap', R, h, t, lift)]
    ad = ap + math.pi
    parts.append(strap_ring('tail', R + t, h, t * 0.8, lift, arc=(ad - 0.05, ad + 1.25)))
    parts.append(link('foot', foot_bm(R, t, ap - 0.36, ap + 0.36, lift, 0.0007), 'modalu'))
    lp = frame('dring', 0.0074 + 2 * t, h + 0.0034, 0.0032, 0.0014, 'modalu', (0, 0, 0))
    e = bpy.data.objects.new('dring', None); col.objects.link(e)
    e.location = ((R + t / 2) * math.cos(ad), (R + t / 2) * math.sin(ad), lift + h / 2); e.rotation_euler = (math.pi / 2, 0, ad + math.pi / 2)
    for o in lp: o.parent = e
    parts.append(e)
    g = group('bracelet', parts); g.location.z = z0
    return g

def build_cable():
    """USB-C power adapter (EU pins) and braided USB-C cable."""
    brick = rbox('brick', 0.032, 0.032, 0.028, 0.006, 0.0012, 'plug', sp=12, se=2)
    brick.rotation_euler = (0, math.pi / 2, 0); brick.location = (0.0, 0, 0.016)
    pins = [cyl(f'p{i}', 0.002, 0.019, 'pin', (-0.0085, y, 0.016), axis='X', seg=32) for i, y in enumerate((-0.0095, 0.0095))]
    boot1 = rbox('boot1', 0.011, 0.0068, 0.016, 0.0028, 0.0008, 'plug', sp=8, se=2); boot1.rotation_euler = (0, math.pi / 2, 0); boot1.location = (0.022, 0, 0.016)
    cable = cyl('cable', 0.0022, 0.2, 'cable', (0.138, 0, 0.016), axis='X', seg=48)
    boot2 = rbox('boot2', 0.011, 0.0068, 0.02, 0.0028, 0.0008, 'plug', sp=8, se=2); boot2.rotation_euler = (0, math.pi / 2, 0); boot2.location = (0.238, 0, 0.016)
    shell = rbox('shell', 0.0026, 0.0084, 0.0066, 0.00125, 0.0, 'pin', sp=8); shell.rotation_euler = (0, math.pi / 2, 0); shell.location = (0.2575, 0, 0.016)
    return group('cable', [brick, boot1, cable, boot2, shell] + pins)

def build_phone():
    body = rbox('phone_body', 0.0715, 0.147, 0.0078, 0.011, 0.0026, 'phone', sp=16, se=4)
    scr = rbox('screen', 0.0668, 0.1423, 0.0004, 0.0094, 0.0, 'screen', (0, 0, 0.0078))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.019, minor_radius=0.0009, major_segments=96, minor_segments=8,
                                     location=(0, 0.024, 0.0083))
    dial = bpy.context.active_object; dial.data.materials.append(M('ui'))
    cards = [rbox(f'card{i}', 0.054, 0.013, 0.0004, 0.003, 0.0, 'card', (0, y, 0.0082)) for i, y in enumerate((-0.022, -0.041))]
    return group('phone', [body, scr, dial] + cards)

def build_bulb():
    base = cyl('bulb_base', 0.0135, 0.024, 'metal', (0, 0, 0.012))
    rings = []
    for i in range(4):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.0136, minor_radius=0.0012, major_segments=64, minor_segments=8,
                                         location=(0, 0, 0.004 + i * 0.005))
        o = bpy.context.active_object; o.data.materials.append(M('metal')); shade(o); rings.append(o)
    prof = [(0.0142, 0.024), (0.0152, 0.032), (0.0175, 0.041)]
    zc, R = 0.071, 0.031
    for k in range(25):
        z = 0.049 + (zc + R - 0.049) * k / 24
        prof.append((math.sqrt(max(R * R - (z - zc) ** 2, 0.0)), z))
    bm = bmesh.new(); vs = [bm.verts.new((r, 0, z)) for r, z in prof]
    es = [bm.edges.new((vs[i], vs[i + 1])) for i in range(len(vs) - 1)]
    bmesh.ops.spin(bm, geom=vs + es, axis=(0, 0, 1), cent=(0, 0, 0), steps=64, angle=2 * math.pi, use_duplicate=False)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    glass = link('bulb_glass', bm, 'glass')
    return group('lamp', [base, glass] + rings)

def build_shutters():
    Wd, Hh = 0.30, 0.30
    parts = [rbox('cassette', Wd, 0.075, 0.055, 0.0, 0.004, 'frame', (0, 0.008, Hh), sp=1),
             rbox('sill', Wd + 0.02, 0.07, 0.014, 0.0, 0.002, 'frame', (0, 0.006, 0), sp=1)]
    for x in (-Wd / 2 + 0.011, Wd / 2 - 0.011):
        parts.append(rbox(f'rail{x:.2f}', 0.022, 0.05, Hh - 0.014, 0.0, 0.002, 'frame', (x, 0, 0.014), sp=1))
    parts.append(rbox('pane', Wd - 0.044, 0.004, Hh - 0.014, 0.0, 0.0, 'pane', (0, 0.012, 0.014), sp=1))
    parts.append(rbox('mullion', 0.012, 0.012, Hh - 0.014, 0.0, 0.001, 'frame', (0, 0.008, 0.014), sp=1))
    for i in range(8):
        parts.append(rbox(f'slat{i}', Wd - 0.044, 0.012, 0.0205, 0.0, 0.0035, 'slat', (0, -0.006, Hh - 0.0225 * (i + 1)), sp=1, se=3))
    return group('shutters', parts)

def build_diffuser():
    body = rbox('dif_body', 0.072, 0.072, 0.058, 0.015, 0.003, 'alu', (0, 0, 0.004), sp=16, se=4)
    pl = rbox('dif_plinth', 0.06, 0.06, 0.004, 0.012, 0.001, 'rubber')
    caps = [cyl(f'cap{i}', 0.0115, 0.012, 'cap', (x, 0.004, 0.062 + 0.006)) for i, x in enumerate((-0.016, 0.016))]
    mist = cyl('mist', 0.0035, 0.0006, 'rubber', (0, -0.021, 0.0623), seg=24)
    slots = [rbox(f'slot{i}', 0.032, 0.002, 0.0018, 0.0, 0.0, 'rubber', (0, -0.0361, 0.016 + i * 0.006), sp=1) for i in range(3)]
    cable = curve('dif_cable', [(0, 0.034, 0.012), (0, 0.06, 0.012), (0.02, 0.09, 0.0016), (0.06, 0.12, 0.0016)], 0.0018, 'cable')
    return group('diffuser', [body, pl, mist, cable] + caps + slots)

# ---------------------------------------------------------------------------------------------------------------
def cycles(samples, res):
    scene.render.engine = 'CYCLES'
    cy = scene.cycles; cy.samples = samples; cy.use_denoising = True
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for t in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
            try:
                prefs.compute_device_type = t; prefs.get_devices()
                if any(d.type == t for d in prefs.devices):
                    for d in prefs.devices: d.use = True
                    cy.device = 'GPU'; print('GPU', t); break
            except TypeError: pass
    except Exception as e: print('CPU only', e)
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100

def look(cam_loc, target, lens, fstop=None, focus=None):
    cd = bpy.data.cameras.new('cam'); cd.lens = lens
    cam = bpy.data.objects.new('cam', cd); col.objects.link(cam); cam.location = cam_loc
    d = Vector(target) - Vector(cam_loc); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    if fstop:
        cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop; cd.dof.focus_distance = focus or d.length
    scene.camera = cam
    return cam

def area(name, loc, target, size, power, color=(1, 1, 1)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.size = size; ld.energy = power; ld.color = color
    lo = bpy.data.objects.new(name, ld); col.objects.link(lo); lo.location = loc
    lo.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return lo

def world(color, strength):
    w = bpy.data.worlds.new('w'); w.use_nodes = True; scene.world = w
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = color; bg.inputs[1].default_value = strength

def plane(name, size, loc, rot, mat):
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size / 2)
    ob = link(name, bm, mat, loc, smooth=False); ob.rotation_euler = rot
    return ob

def colour_management(view):
    for v in (view, 'AgX', 'Filmic', 'Standard'):
        try: scene.view_settings.view_transform = v; break
        except TypeError: continue
    if view != 'Standard':
        for lk in ('AgX - Medium High Contrast', 'Medium High Contrast', 'None'):
            try: scene.view_settings.look = lk; break
            except TypeError: continue

def studio(view):
    scene.render.film_transparent = True
    world(srgb('#9a9aa0'), 0.1)
    lens = 135
    if view == 'cable':
        build_cable(); fw, tgt, pos = 0.34, (0.115, 0, 0.016), (0.115, -1, 0.016)
    elif view == 'foot':
        build_bracelet(); a = math.radians(-60); fw = 0.045
        tgt = (0.031 * math.cos(a), 0.031 * math.sin(a), 0.004); pos = (0.031 * math.cos(a) * 3.2, 0.031 * math.sin(a) * 3.2, 0.03)
    elif view == 'band':
        build_bracelet(); fw, tgt, pos = 0.13, (0, 0, 0.011), (0.6, -0.9, 0.55)
    elif view in ('persp', 'lit', 'persp_back', 'persp_band'):
        build_base(with_time=(view == 'lit')); fw, tgt = W / 0.55, (0, 0, TOP * 0.42)
        if view == 'persp_band': build_bracelet(TOP); fw, tgt = W / 0.52, (0, 0, TOP * 0.75)
        pos = (-0.62, 0.95, 0.24) if view == 'persp_back' else (0.62, -0.95, 0.24)
    else:
        build_base()
        if view == 'top': build_bracelet(TOP)
        if view in ('front', 'back'):
            fw = W / 0.62; tgt = (0, 0, TOP * 0.5); pos = (0, -1 if view == 'front' else 1, TOP * 0.42)
        else:
            fw = (W / 0.80) * 16 / 9; tgt = (0, 0, TOP / 2); pos = (0, 0.0001, 1 if view == 'top' else -1)
    d = fw * lens / 36; v = Vector(pos) - Vector(tgt); v.normalize(); cam = look(tuple(Vector(tgt) + v * d), tgt, lens)
    if PLASTIC:  # floating views with the table shot's light: dim world, soft key top-left, faint fill
        world(srgb('#f2f2f0'), 0.25); soft_light()
        # the table's bounce, without the table: soft light from below the front, invisible to the camera
        area('fill2', (0.4, -0.7, 0.35), tgt, 1.5, 14).visible_camera = False
        area('bounce', (0.1, -0.5, -0.45), tgt, 2.0, 30).visible_camera = False
        return
    area('key', (0, -0.5, 1.2), (0, 0, 0.02), 1.6, 110)
    area('left', (-0.9, -0.5, 0.15), (0, 0, 0.02), 0.6, 35)
    area('right', (0.9, -0.5, 0.15), (0, 0, 0.02), 0.6, 35)
    area('cam', tuple(Vector(cam.location) * 0.9 + Vector((0, 0, 0.3))), tgt, 1.2, 25)
    if view in ('persp', 'lit', 'band', 'persp_back', 'persp_band', 'foot'): area('front', tuple(Vector(cam.location) * 0.8 + Vector((-0.3, 0, 0.2))), tgt, 1.4, 40)
    if view in ('persp', 'lit'):
        area('topback', (-0.1, 0.9, 0.9), (0, 0, 0.03), 1.6, 45)
        area('sidestrip', (1.0, 0.45, 0.25), (0, 0, 0.02), 0.5, 30)
    if view == 'persp_back': area('backkey', (0.2, 0.9, 0.6), (0, 0, 0.02), 1.4, 120)
    if view in ('back', 'bottom'): area('cam2', tuple(Vector(cam.location) * 0.9), tgt, 1.2, 40)

def soft_light():
    area('key', (-0.45, 0.3, 0.8), (0, 0, 0), 0.6, 75)
    area('fill', (0.8, -0.6, 0.5), (0, 0, 0), 1.5, 6)

def table_scene():
    build_base()
    boot = rbox('boot', 0.011, 0.016, 0.0062, 0.0025, 0.0008, 'plug', (0, W / 2 + 0.008, MID - 0.0031), sp=8, se=2)
    curve('usb', [(0, W / 2 + 0.015, MID), (0, W / 2 + 0.045, MID - 0.004), (0.015, W / 2 + 0.075, 0.003),
                  (0.05, W / 2 + 0.16, 0.0028), (0.03, W / 2 + 0.32, 0.0028)], 0.0021, 'cable')
    MATS['table'] = principled('table', srgb('#cfcfcc'), rough=0.85)
    bm = rbox_bm(1.4, 1.4, 0.04, 0.0, 0.002, sp=1, se=2)
    t = link('table', bm, 'table', (0.33, -0.5, -0.04)); t.rotation_euler = (0, 0, math.radians(-22))
    # world: dim for lighting, white where the camera sees it past the table edge
    w = bpy.data.worlds.new('w'); w.use_nodes = True; scene.world = w; nt = w.node_tree
    bg = nt.nodes['Background']; bg.inputs[0].default_value = srgb('#f2f2f0'); bg.inputs[1].default_value = 0.25
    sky = nt.nodes.new('ShaderNodeBackground'); sky.inputs[0].default_value = srgb('#f6f6f4'); sky.inputs[1].default_value = 2.0
    lp = nt.nodes.new('ShaderNodeLightPath'); mx = nt.nodes.new('ShaderNodeMixShader'); out = nt.nodes['World Output']
    nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); nt.links.new(bg.outputs[0], mx.inputs[1]); nt.links.new(sky.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs[0])
    soft_light()
    look((0.36, -0.45, 0.40), (0.0, 0.04, 0.0), 55, 8.0)
    scene.view_settings.exposure = -0.8

def real():
    res = (1200, 675) if PREVIEW else (2400, 1350)
    cycles(64 if PREVIEW else 384, res)
    colour_management('AgX')
    if TABLE:
        table_scene()
    elif STUDIO:
        studio(SHOT)
        if PLASTIC: scene.view_settings.exposure = -0.8
    else:
        build_base(with_time=(SHOT == 'dawn'))
        MATS['wood'] = wood()
        MATS['wall'] = principled('wall', srgb('#2b2a2e' if SHOT == 'night' else '#6b5a4a'), rough=0.95)
        plane('table', 1.2, (0, 0.05, 0), (0, 0, 0), 'wood')
        plane('wall', 3.0, (0, 0.38, 0), (math.pi / 2, 0, 0), 'wall')
        if SHOT == 'night':
            world(srgb('#0b0d18'), 0.02)
            area('moon', (-0.9, -0.2, 0.7), (0, 0, 0), 0.8, 10, (0.62, 0.68, 1.0))
            area('rim', (0.2, 0.5, 0.25), (0, 0, 0.05), 0.4, 6, (0.55, 0.6, 1.0))
        else:
            world(srgb('#2a1c12'), 0.06)
            area('sun', (1.0, 0.3, 0.35), (0, 0, 0.03), 0.5, 45, (1.0, 0.62, 0.32))
            area('bounce', (-0.5, -0.6, 0.3), (0, 0, 0.03), 0.8, 14, (1.0, 0.85, 0.7))
        look((0.33, -0.46, 0.14), (0.0, 0.01, 0.024), 70, 2.8)
    scene.render.filepath = os.path.join(OUT, f'aurawake-{SHOT}{"-plastic" if PLASTIC else ""}{"-preview" if PREVIEW else ""}.png')
    bpy.ops.render.render(write_still=True)

# ---------------------------------------------------------------------------------------------------------------
# Technical drawings: true isometric ortho camera, flat fills, Freestyle lines (outline heavier than inner lines).
ISO = (math.radians(54.7356), 0.0, math.radians(45))
SS = 2.5  # render scale over the size shown on the slide

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

def line():
    scene.render.engine = 'CYCLES'; scene.cycles.samples = 16; scene.cycles.use_denoising = False
    scene.render.film_transparent = True
    colour_management('Standard')
    world((1, 1, 1, 1), 0.0)
    cd = bpy.data.cameras.new('iso'); cd.type = 'ORTHO'
    cam = bpy.data.objects.new('iso', cd); col.objects.link(cam); cam.rotation_euler = ISO; scene.camera = cam
    bpy.context.view_layer.update()
    R = cam.matrix_world.to_3x3(); right, up, back = R.col[0], R.col[1], R.col[2]

    # (group builder, size shown on the slide in px, named points for callouts)
    items = {
        'base': (lambda: build_base(with_time=True, time='06:30'), 400, {
            'top': (0.02, 0.02, TOP), 'time': (-0.012, -W / 2, MID + 0.003), 'led': (0.036, -W / 2, MID),
            'grille': (W / 2, 0.012, MID + 0.006)}),
        'bracelet': (build_bracelet, 240, {}),
        'phone': (build_phone, 250, {}),
        'lamp': (build_bulb, 170, {}),
        'shutters': (build_shutters, 300, {}),
        'diffuser': (build_diffuser, 200, {'caps': (0.016, 0.004, 0.074)}),
    }
    anchors = {}
    for name, (fn, size, pts) in items.items():
        for o in list(col.objects):
            if o.type != 'CAMERA': bpy.data.objects.remove(o, do_unlink=True)
        g = fn(); bpy.context.view_layer.update()
        cs = [o.matrix_world @ Vector(c) for o in g.children_recursive if o.type == 'MESH' or o.name.startswith('band') for c in o.bound_box]
        xs = [c.dot(right) for c in cs]; ys = [c.dot(up) for c in cs]
        span = max(max(xs) - min(xs), max(ys) - min(ys)) * 1.16
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        cam.location = right * cx + up * cy + back * 2.0
        cd.ortho_scale = span; cd.clip_end = 10
        px = round(size * SS); scene.render.resolution_x = scene.render.resolution_y = px
        freestyle(2.6, 5.2)
        bpy.context.view_layer.update()
        def proj(p):
            v = world_to_camera_view(scene, cam, Vector(p)); return [round(v.x * size, 1), round((1 - v.y) * size, 1)]
        anchors[name] = {'size': size, 'ground': proj((0, 0, 0)), 'points': {k: proj(p) for k, p in pts.items()}}
        scene.render.filepath = os.path.join(OUT, f'iso-{name}.png')
        bpy.ops.render.render(write_still=True)
    with open(os.path.join(OUT, 'anchors.json'), 'w') as f: json.dump(anchors, f, indent=1)

real() if MODE == 'real' else line()
