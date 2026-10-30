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
STATE = next((a.split('=', 1)[1] for a in argv if a.startswith('state=')), '')   # light state for 'led' / 'strip'
PLASTIC = 'plastic' in argv
GRIDT = 'grid' in argv          # time option 4: a 3×5 dot font on the speaker grille's own grid (pitch, graded dot size)
SEGS = 'seg' in argv            # time option 1: continuous segments under a thin dead-front window
COARSE = 'coarse' in argv
BODY_HEX = next((a.split('=', 1)[1] for a in argv if a.startswith('col=')), '#292a2e')   # graphite body (owner, 2026-10-29: a touch darker)
GRAIN = float(next((a.split('=', 1)[1] for a in argv if a.startswith('grain=')), '0.25'))  # satin bump on plastic (0.30 → 0.25: a little finer)
FINE = not (COARSE or SEGS or GRIDT)   # the time (owner, 2026-10-29): fine dot matrix behind ~0.1 mm laser micro-holes
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
BTN_R, BTN_HOLE = 0.0049, 0.0054   # button and its recess: a 0.5 mm gap (owner, 2026-10-29; was 0.8)
BTN_CLEAR = PORT_CLEAR = 0.011   # two equal free circles round the USB-C and the button: room for the marks on one line
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
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = GRAIN if PLASTIC else 0.05; bp.inputs['Distance'].default_value = 0.0001
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

def braid(name, dark, R=0.0021, w=0.00085):
    """Braided textile cable (owner, 2026-10-29): a 2/2 diamond braid of flat strands at ±45° round the cord (object
    axis Y), each strand rounded in the bump, fine fibres along it, a slight tone change from strand to strand."""
    m = principled(name, dark, rough=0.78); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    for k in ('Sheen Weight', 'Sheen'):
        if k in b.inputs: b.inputs[k].default_value = 0.2; break
    tc = nt.nodes.new('ShaderNodeTexCoord'); P = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], P.inputs[0])
    def op(o, a, c=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = o
        for i, x in enumerate((a, c)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    arc = op('MULTIPLY', op('ARCTAN2', P.outputs[2], P.outputs[0]), R)          # distance round the cord
    fu, fv = op('DIVIDE', op('ADD', P.outputs[1], arc), w), op('DIVIDE', op('SUBTRACT', P.outputs[1], arc), w)
    iu, iv = op('FLOOR', fu), op('FLOOR', fv)
    top = op('LESS_THAN', op('FLOORED_MODULO', op('ADD', op('FLOOR', op('DIVIDE', iu, 2.0)), op('FLOOR', op('DIVIDE', iv, 2.0))), 2.0), 0.5)
    ru = op('SINE', op('MULTIPLY', op('FRACT', fv), math.pi)); rv = op('SINE', op('MULTIPLY', op('FRACT', fu), math.pi))
    height = op('ADD', op('MULTIPLY', top, ru), op('MULTIPLY', op('SUBTRACT', 1.0, top), rv))
    fib = nt.nodes.new('ShaderNodeTexWave'); fib.wave_type = 'BANDS'; fib.inputs['Scale'].default_value = 9000
    fib.inputs['Distortion'].default_value = 2.0; nt.links.new(tc.outputs['Object'], fib.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.8; bp.inputs['Distance'].default_value = 0.00025
    nt.links.new(op('ADD', op('POWER', height, 0.6), op('MULTIPLY', fib.outputs['Fac'], 0.12)), bp.inputs['Height'])
    nt.links.new(bp.outputs[0], b.inputs['Normal'])
    cell = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(iu, cell.inputs[0]); nt.links.new(iv, cell.inputs[1])
    wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; nt.links.new(cell.outputs[0], wn.inputs['Vector'])
    g = op('ADD', 0.62, op('ADD', op('MULTIPLY', height, 0.3), op('MULTIPLY', wn.outputs['Value'], 0.12)))
    cc = nt.nodes.new('ShaderNodeCombineColor')
    for k in range(3): nt.links.new(g, cc.inputs[k])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
    mx.inputs[6].default_value = dark; nt.links.new(cc.outputs[0], mx.inputs[7]); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    return m

def loop_fabric(name, dark, light, edge, R=0.031, h=0.020, lift=0.0016, p=0.00042):
    """Woven melange strap: a 2/1 twill whose threads wander slightly (noise-warped grid), each thread rounded in the
    bump, colour in soft clouds between two blues, a few near-white weft flecks, fibre fuzz, darker corded edges."""
    m = principled(name, dark, rough=0.92); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    for k in ('Sheen Weight', 'Sheen'):
        if k in b.inputs: b.inputs[k].default_value = 0.6; break
    if 'Sheen Roughness' in b.inputs: b.inputs['Sheen Roughness'].default_value = 0.4
    tc = nt.nodes.new('ShaderNodeTexCoord'); P = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], P.inputs[0])
    def op(o, a, c=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = o
        for i, x in enumerate((a, c)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    def noise(scale, detail=3):
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail
        nt.links.new(tc.outputs['Object'], n.inputs['Vector']); return n
    warp = noise(1400); wc = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(warp.outputs['Color'], wc.inputs[0])
    u = op('ADD', op('MULTIPLY', op('ARCTAN2', P.outputs[1], P.outputs[0]), R), op('MULTIPLY', op('SUBTRACT', wc.outputs[0], 0.5), p * 0.7))
    v = op('ADD', P.outputs[2], op('MULTIPLY', op('SUBTRACT', wc.outputs[1], 0.5), p * 0.7))
    fu, fv = op('DIVIDE', u, p), op('DIVIDE', v, p)
    iu, iv = op('FLOOR', fu), op('FLOOR', fv)
    weft = op('LESS_THAN', op('FLOORED_MODULO', op('SUBTRACT', iu, iv), 3.0), 0.5)
    ru = op('SINE', op('MULTIPLY', op('FRACT', fu), math.pi)); rv = op('SINE', op('MULTIPLY', op('FRACT', fv), math.pi))
    height = op('ADD', op('MULTIPLY', weft, rv), op('MULTIPLY', op('SUBTRACT', 1.0, weft), ru))
    fuzz = noise(14000, 8)
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.75; bp.inputs['Distance'].default_value = 0.0003
    nt.links.new(op('ADD', op('POWER', height, 0.7), op('MULTIPLY', fuzz.outputs['Fac'], 0.45)), bp.inputs['Height'])
    nt.links.new(bp.outputs[0], b.inputs['Normal'])
    # colour: clouds between the two blues, per-thread variation, rare white flecks on weft threads
    cloud = noise(700, 4)
    cell = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(iu, cell.inputs[0]); nt.links.new(iv, cell.inputs[1])
    wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; nt.links.new(cell.outputs[0], wn.inputs['Vector'])
    base = nt.nodes.new('ShaderNodeMix'); base.data_type = 'RGBA'; base.inputs[6].default_value = dark; base.inputs[7].default_value = light
    nt.links.new(op('ADD', op('MULTIPLY', cloud.outputs['Fac'], 0.75), op('MULTIPLY', wn.outputs['Value'], 0.35)), base.inputs['Factor'])
    fleck = nt.nodes.new('ShaderNodeMix'); fleck.data_type = 'RGBA'; fleck.inputs[7].default_value = srgb('#c8dbf3')
    nt.links.new(base.outputs[2], fleck.inputs[6])
    nt.links.new(op('MULTIPLY', weft, op('GREATER_THAN', wn.outputs['Value'], 0.9)), fleck.inputs['Factor'])
    edge_m = op('MAXIMUM', op('LESS_THAN', P.outputs[2], lift + 0.0014), op('GREATER_THAN', P.outputs[2], lift + h - 0.0014))
    fin = nt.nodes.new('ShaderNodeMix'); fin.data_type = 'RGBA'; fin.inputs[7].default_value = edge
    nt.links.new(fleck.outputs[2], fin.inputs[6]); nt.links.new(op('MULTIPLY', edge_m, 0.8), fin.inputs['Factor'])
    sh = nt.nodes.new('ShaderNodeMix'); sh.data_type = 'RGBA'; sh.blend_type = 'MULTIPLY'; sh.inputs['Factor'].default_value = 1.0
    nt.links.new(fin.outputs[2], sh.inputs[6])
    g = op('ADD', 0.72, op('MULTIPLY', height, 0.28)); cc = nt.nodes.new('ShaderNodeCombineColor')
    for k in range(3): nt.links.new(g, cc.inputs[k])
    nt.links.new(cc.outputs[0], sh.inputs[7]); nt.links.new(sh.outputs[2], b.inputs['Base Color'])
    return m

TABLE = SHOT == 'table'
STUDIO = SHOT in ('ports', 'time', 'left', 'right', 'top_cable', 'led', 'strip', 'pod_in', 'pod_side', 'foot', 'persp_band', 'table', 'front', 'back', 'top', 'bottom', 'cable', 'persp', 'lit', 'band', 'persp_back')
if MODE == 'real':
    MATS = {
        'body': body_real('body', srgb(BODY_HEX)),
        'shell': satin('shell', srgb(BODY_HEX)),
        'alu': bump_tex(principled('alu', srgb('#18181b'), metal=1.0, rough=0.5), 'noise', 4000, 0.04),
        'grille': grille('grille', srgb('#060607'), srgb('#000000')),
        'rubber': principled('rubber', srgb('#0a0a0b'), rough=0.8),
        'cavity': principled('cavity', srgb('#050506'), rough=0.9),
        'print': principled('print', srgb('#7a7a7e'), rough=0.6),
        'mark': principled('mark', srgb('#8a8b90'), rough=0.8),    # laser etching: a light, matte grey on the graphite (owner, 2026-10-29)
        'gold': principled('gold', srgb('#d9b25e'), metal=1.0, rough=0.28),
        'pin': principled('pin', srgb('#c8c8cc'), metal=1.0, rough=0.25),
        'led_under': principled('led_under', srgb('#141416'), rough=0.6) if STUDIO and SHOT != 'lit' else
                     emit('led_under', srgb(NIGHT if SHOT == 'night' else DAWN), 90.0 if SHOT == 'night' else 160.0 if SHOT == 'lit' else 70.0),
        'led_front': emit('led_front', srgb('#ffffff'), 3.0 if STUDIO else 0.0),
        'dots': emit('dots', srgb('#ffd9a0'), 7.0),
        'band': principled('band', srgb('#2a2b2f'), rough=0.62),
        'fabric': fabric('fabric', srgb('#1c1d20')),
        'loop': loop_fabric('loop', srgb('#4a80c8'), srgb('#7aa8de'), srgb('#3f74bb')),
        'lens': principled('lens', srgb('#050506'), rough=0.06, coat=0.0),
        'steel': bump_tex(principled('steel', srgb('#1c1d20'), metal=1.0, rough=0.36), 'noise', 9000, 0.04),
        'modalu': bump_tex(principled('modalu', srgb('#4a4b50'), metal=1.0, rough=0.34), 'noise', 9000, 0.05),
        'cable': braid('cable', srgb('#1a1b1e')),
        'plug': principled('plug', srgb('#0a0a0b'), rough=0.6),
    }
else:
    T = {'alu': 0.86, 'grille': 0.42, 'rubber': 0.3, 'print': 0.4, 'pin': 0.75, 'band': 0.5, 'cable': 0.25, 'dots': 0.28,
         'led_front': 0.25, 'phone': 0.88, 'screen': 0.30, 'ui': 0.92, 'card': 0.5, 'metal': 0.74, 'glass': 0.98,
         'frame': 0.96, 'fabric': 0.5, 'loop': 0.62, 'steel': 0.3, 'lens': 0.1, 'modalu': 0.4, 'slat': 0.80, 'pane': 0.90, 'cap': 0.70, 'plug': 0.3, 'mark': 0.62, 'skin': 0.985, 'gold': 0.7}
    MATS = {k: toon(k, grey(v)) for k, v in T.items()}
    MATS['body'] = body_toon('body', grey(0.86))
    MATS['shell'] = toon('shell', grey(0.86))
    MATS['led_under'] = toon('led_under', srgb(DAWN))

LIGHT_COL = {'white': '#fff2df', 'night': NIGHT, 'dawn': DAWN}

def strip_mat(state):
    """Light strip around the rubber disc. off = dark; white / night / dawn = lit; charging = lit on one half only
    (the bracelet charging: the line fills from one side)."""
    if state not in LIGHT_COL and state != 'charging':
        return principled('led_under', srgb('#141416'), rough=0.6)
    col = 'white' if state == 'charging' else state
    m = emit('led_under', srgb(LIGHT_COL[col]), 70.0 if state != 'white' else 45.0)
    if state == 'charging':
        nt = m.node_tree; e = next(n for n in nt.nodes if n.type == 'EMISSION'); out = nt.nodes['Material Output']
        off = nt.nodes.new('ShaderNodeBsdfPrincipled'); off.inputs['Base Color'].default_value = srgb('#141416')
        mx = nt.nodes.new('ShaderNodeMixShader'); tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ')
        nt.links.new(tc.outputs['Object'], sp.inputs[0])
        a = nt.nodes.new('ShaderNodeMath'); a.operation = 'ARCTAN2'; nt.links.new(sp.outputs[1], a.inputs[0]); nt.links.new(sp.outputs[0], a.inputs[1])
        lt = nt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.0; nt.links.new(sp.outputs[0], lt.inputs[0])  # the left half is lit
        nt.links.new(lt.outputs[0], mx.inputs[0]); nt.links.new(e.outputs[0], mx.inputs[1]); nt.links.new(off.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs[0])
    return m

if MODE == 'real' and SHOT == 'led':
    LED_SAT = {'white': '#fff6ea', 'night': '#4d5cff', 'dawn': '#ff9a1f', 'green': '#34d27a', 'red': '#ff3a2a'}   # spec §4.1   # saturated: the state must read at a glance
    MATS['led_front'] = emit('led_front', srgb(LED_SAT[STATE]), 1.8 if STATE != 'white' else 4.0) if STATE in LED_SAT else principled('led_front', srgb('#0b0b0c'), rough=0.08)
if MODE == 'real' and SHOT == 'strip':
    MATS['led_under'] = strip_mat(STATE)
    MATS['led_front'] = principled('led_front', srgb('#0b0b0c'), rough=0.08)   # only the strip speaks

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
        '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'],
        'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
        'F': ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
        '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
        '%': ['11000', '11001', '00010', '00100', '01000', '10011', '00011'],   # the charge, written for 8 s
        ':': ['0', '0', '1', '0', '1', '0', '0']}

FONT_FINE = dict(FONT, **{'0': ['01110', '10001', '10001', '10001', '10001', '10001', '01110']})

SEG7 = {'0': 'abcdef', '1': 'bc', '3': 'abcdg', '4': 'bcfg', '6': 'acdefg'}

def time_segs(text, zc, h=0.0125, w=0.0062, t=0.0008, gap=0.0003, sp=0.0027, colon=0.0042, xo=-0.006):
    """Seven-segment digits drawn as thin strokes with 45° cut ends (Braun / TE), lit through the thin shell."""
    widths = [colon if ch == ':' else w for ch in text]
    x = xo - (sum(widths) + sp * (len(text) - 1)) / 2; bm = bmesh.new(); y0 = -W / 2 - 0.00005
    def poly(pts):
        vs = [bm.verts.new((px, y0, pz)) for px, pz in pts]; bm.faces.new(vs)
    def hz(x0, x1, z): poly([(x0, z), (x0 + t / 2, z + t / 2), (x1 - t / 2, z + t / 2), (x1, z), (x1 - t / 2, z - t / 2), (x0 + t / 2, z - t / 2)])
    def vt(xx, z0, z1): poly([(xx, z0), (xx + t / 2, z0 + t / 2), (xx + t / 2, z1 - t / 2), (xx, z1), (xx - t / 2, z1 - t / 2), (xx - t / 2, z0 + t / 2)])
    for ch, cw in zip(text, widths):
        if ch == ':':
            for dz in (-h * 0.2, h * 0.2):
                c = x + cw / 2; r = t * 0.55
                poly([(c + r * math.cos(a * math.pi / 8), zc + dz + r * math.sin(a * math.pi / 8)) for a in range(16)])
        else:
            top, mid, bot = zc + h / 2, zc, zc - h / 2
            P = {'a': lambda: hz(x + gap, x + cw - gap, top), 'g': lambda: hz(x + gap, x + cw - gap, mid), 'd': lambda: hz(x + gap, x + cw - gap, bot),
                 'f': lambda: vt(x, mid + gap, top - gap), 'b': lambda: vt(x + cw, mid + gap, top - gap),
                 'e': lambda: vt(x, bot + gap, mid - gap), 'c': lambda: vt(x + cw, bot + gap, mid - gap)}
            for k in SEG7[ch]: P[k]()
        x += cw + sp
    return link('time', bm, 'dots', smooth=False)

FONT3 = {'0': ['111', '101', '101', '101', '111'], '1': ['010', '110', '010', '010', '111'], '3': ['111', '001', '111', '001', '111'],
         '4': ['101', '101', '111', '001', '001'], '6': ['111', '100', '111', '101', '111'], ':': ['0', '1', '0', '1', '0']}

def time_grid(text, c0=-11, row0=1.5):
    """The time drawn with the speaker holes' own grid: same column pitch, same rows, same graded dot size."""
    cols_ = []
    for i, ch in enumerate(text):
        if i: cols_.append(None)
        g = FONT3[ch]
        for c in range(len(g[0])): cols_.append([g[r][c] == '1' for r in range(5)])
    bm = bmesh.new()
    for ci, c in enumerate(cols_):
        if c is None: continue
        for r, on in enumerate(c):
            if not on: continue
            cv = (row0 - r) * PV
            m = Matrix.Translation(((c0 + ci) * PU, -W / 2 - 0.00005, MID + cv)) @ Matrix.Rotation(math.pi / 2, 4, 'X')
            bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=hole_r(cv), radius2=hole_r(cv), depth=0.0003, matrix=m)
    return link('time', bm, 'dots', smooth=False)

def time_dots(text, zc, pitch=0.0017, r=0.0005, xo=-0.006):
    if SEGS: return time_segs(text, zc)
    if GRIDT: return time_grid(text)
    if FINE: pitch, r, xo = PU / 3, 0.00036, -5 * PU / 3   # one square lattice: every third column on a speaker column, centred on MID
    font = FONT_FINE if FINE else FONT
    cols = []
    for i, ch in enumerate(text):
        if i: cols.append(None)
        g = font[ch]
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
            if u * u + cv * cv > PORT_CLEAR ** 2 and (u - BTN_X) ** 2 + cv * cv > BTN_CLEAR ** 2:
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

MARK_FONT = 'C:/Windows/Fonts/bahnschrift.ttf'   # DIN-like: the usual face for product markings

def back_marks():
    """Laser-etched marks on the back (owner, 2026-10-29), drawn in the face plane as seen from behind (sx to the
    viewer's right, sz up): a charging bolt over the USB-C with its rating under it, the Bluetooth rune over the
    button. Both icons 2.8 mm tall on one line, 1.4 mm over the button's recess; the rating 1.3 mm cap height, 1.6 mm
    under the port."""
    y = W / 2 + 0.00003; bm = bmesh.new(); t = 0.00022
    P = lambda sx, sz: Vector((-sx, y, MID + sz))
    def poly(pts):
        bm.faces.new([bm.verts.new(P(a, b)) for a, b in pts])
    def disc(a, b, r, n=12): poly([(a + r * math.cos(2 * math.pi * k / n), b + r * math.sin(2 * math.pi * k / n)) for k in range(n)])
    def stroke(pts, w=t):
        for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
            d = math.hypot(a1 - a0, b1 - b0); nx, nz = -(b1 - b0) / d * w / 2, (a1 - a0) / d * w / 2
            poly([(a0 + nx, b0 + nz), (a1 + nx, b1 + nz), (a1 - nx, b1 - nz), (a0 - nx, b0 - nz)])
        for a, b in pts: disc(a, b, w / 2)
    def rrect(a0, b0, a1, b1, r, n=4):
        pts = []
        for cx, cz, q in ((a1 - r, b1 - r, 0), (a0 + r, b1 - r, 90), (a0 + r, b0 + r, 180), (a1 - r, b0 + r, 270)):
            pts += [(cx + r * math.cos(math.radians(q + 90 * k / n)), cz + r * math.sin(math.radians(q + 90 * k / n))) for k in range(n + 1)]
        poly(pts)
    u = 0.0014; zc = BTN_HOLE + 0.0014 + u        # icon half-height (2.8 mm icons); one line for both, set by the button's recess
    # charging bolt over the USB-C: a zigzag whose stroke thins from the tail to a big arrowhead
    C = [(0.30, 1.0), (-0.24, -0.02), (0.24, 0.10), (-0.16, -0.60)]
    C = [(a * u, zc + b * u) for a, b in C]; L = [0.0]
    for (a0, b0), (a1, b1) in zip(C, C[1:]): L.append(L[-1] + math.hypot(a1 - a0, b1 - b0))
    wid = lambda d: (0.36 + (0.13 - 0.36) * d / L[-1]) * u
    def nrm(i):
        ns = []
        for j in (i - 1, i):
            if 0 <= j < len(C) - 1:
                (a0, b0), (a1, b1) = C[j], C[j + 1]; d = math.hypot(a1 - a0, b1 - b0); ns.append((-(b1 - b0) / d, (a1 - a0) / d))
        nx, nz = sum(n[0] for n in ns), sum(n[1] for n in ns); k = math.hypot(nx, nz)
        cosh = max(0.35, (nx * ns[0][0] + nz * ns[0][1]) / k)
        return nx / k / cosh, nz / k / cosh               # mitre: keeps the stroke width at the corners
    side = [(C[i][0] + nrm(i)[0] * wid(L[i]) / 2, C[i][1] + nrm(i)[1] * wid(L[i]) / 2, C[i][0] - nrm(i)[0] * wid(L[i]) / 2, C[i][1] - nrm(i)[1] * wid(L[i]) / 2) for i in range(len(C))]
    for p0, p1 in zip(side, side[1:]): poly([(p0[0], p0[1]), (p1[0], p1[1]), (p1[2], p1[3]), (p0[2], p0[3])])
    (a0, b0), (a1, b1) = C[-2], C[-1]; d = math.hypot(a1 - a0, b1 - b0); dx, dz = (a1 - a0) / d, (b1 - b0) / d
    hl, hw = 0.55 * u, 0.42 * u                          # the arrowhead
    poly([(a1 + dx * hl, b1 + dz * hl), (a1 - dz * hw, b1 + dx * hw), (a1 + dz * hw, b1 - dx * hw)])
    # Bluetooth rune over the button
    bx = -BTN_X; h = 2 * u
    stroke([(bx + a * h, zc + b * h) for a, b in ((-0.27, 0.25), (0.27, -0.25), (0, -0.5), (0, 0.5), (0.27, 0.25), (-0.27, -0.25))], 0.00026)
    # DC symbol between "5V" and "3A" under the USB-C
    zr = -(0.0013 + 0.0016 + 0.00065); sw = 0.0013   # the rating: same gap under the port
    stroke([(-sw / 2, zr + 0.00022), (sw / 2, zr + 0.00022)], 0.00016)
    for k in range(3):
        a = -sw / 2 + k * sw / 2.5; stroke([(a, zr - 0.00022), (a + sw / 5, zr - 0.00022)], 0.00016)
    obs = [link('marks', bm, 'mark', smooth=False)]
    for txt, sx, al in (('5V', -sw / 2 - 0.0007, 'RIGHT'), ('3A', sw / 2 + 0.0007, 'LEFT')):
        cu = bpy.data.curves.new('t', 'FONT'); cu.body = txt; cu.font = bpy.data.fonts.load(MARK_FONT, check_existing=True)
        cu.size = 0.00185; cu.align_x = al; cu.align_y = 'CENTER'
        ob = bpy.data.objects.new('t', cu); col.objects.link(ob); ob.location = P(sx, zr); ob.rotation_euler = (math.pi / 2, 0, math.pi)
        cu.materials.append(M('mark')); obs.append(ob)
    return obs

def charge_pins():
    """Three gold spring pins for the bracelet (owner, 2026-10-29): one row parallel to the front, centred left-right,
    20 mm from the front edge, 4 mm pitch; each a 1.5 mm dome 0.2 mm proud in a dark 2.2 mm insulating ring."""
    obs = []
    for i in (-1, 0, 1):
        x, y = i * 0.004, -W / 2 + 0.020
        obs.append(cyl(f'pin_ring{i}', 0.0011, 0.0001, 'rubber', (x, y, TOP + 0.00002), seg=32))
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=0.00075)
        for v in bm.verts: v.co.z = max(v.co.z, 0.0) * 0.27
        obs.append(link(f'pin{i}', bm, 'gold', (x, y, TOP)))
    return obs

def build_base(with_time=False, time='06:30'):
    """Solid graphite block: speakers behind dot grilles on the sides and back, time + LED at the front, USB-C and the
    Bluetooth button at the back, haptic + magnetic top for the bracelet, thin rubber disc ringed by the light strip."""
    body = rbox('body', W, W, H, EDGE_P, EDGE_T, 'body', (0, 0, PL), sp=4, se=2)
    cut(body, stadium_bm(0.0084, 0.0026, 0.012), (0, W / 2, MID), 'rubber')  # USB-C receptacle
    cut(body, cutter_bm([(BTN_X, 0, BTN_HOLE)], 0.002), (0, W / 2, MID), 'rubber')
    if MODE == 'real': cut(body, holes_bm(), (0, 0, 0), 'cavity')
    wn = body.modifiers.new('wn', 'WEIGHTED_NORMAL'); wn.keep_sharp = True; wn.mode = 'FACE_AREA'
    btn = cyl('button', BTN_R, 0.002, 'shell', (BTN_X, W / 2 - 0.0008, MID), axis='Y')
    tongue = rbox('tongue', 0.0066, 0.004, 0.0007, 0.0003, 0.0, 'print', (0, W / 2 - 0.0035, MID - 0.00035), sp=4)
    disc = cyl('disc', 0.034, PL, 'rubber', (0, 0, PL / 2), seg=128)
    ring = cyl('ring', 0.0343, PL * 0.5, 'led_under', (0, 0, PL / 2), seg=128)
    dot = cyl('led_front', 0.00085, 0.0003, 'led_front', (0.036, -W / 2 - 0.00002, MID), axis='Y', seg=24)
    obs = [body, btn, tongue, disc, ring, dot] + back_marks() + charge_pins()
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
    return [rbox(f'{name}{i}', w, d, sz, min(w, d) * 0.45, sz * 0.4, mat, (x + dx, y + dy, z), sp=4, se=3) for i, (w, d, dx, dy) in enumerate((
        (sx, bar, 0, -(sy - bar) / 2), (sx, bar, 0, (sy - bar) / 2), (bar, sy, -(sx - bar) / 2, 0), (bar, sy, (sx - bar) / 2, 0)))]

# Bracelet (owner refs: Sport Loop, blue and orange/grey). One continuous woven strip, lying on its edge:
# fixed to the steel loop, round the wrist (an oval, straight where the pod is), back through the loop, folded, and
# its tail runs back on the outside over the pod, closing with hook-and-loop. The pod sits in the pocket between the
# two layers, right next to the loop; its lower end leaves the strip as the flat charging foot.
STRAP_A, STRAP_B, STRAP_XF = 0.033, 0.027, 0.0225   # oval half-axes (y, x) and the straight side where the pod is
STRAP_T, STRAP_H, STRAP_LIFT = 0.0012, 0.019, 0.0016
LOOP_TH = math.radians(42)                          # steel loop: just past the straight side
POD_HALF = math.radians(33.5)                       # the straight side = the pod (≈37 mm)
AP = math.radians(-30)                              # where the pod faces once the bracelet is turned for the views

def strap_e(th):
    """Centre line of the inner layer: an oval, clipped straight on +x (the pod side)."""
    return Vector((min(STRAP_B * math.cos(th), STRAP_XF), STRAP_A * math.sin(th)))

POD_T, POD_LEN = 0.0016, 0.034                      # sensor pod: slim graphite plate on the inner side
BAR_T, BAR_W = 0.0011, 0.0040                       # steel loop: a flat metal ribbon
OV = 0.24                                           # the strip runs this far past the loop before folding (≈7 mm)

def strap_n(th):
    """Outward unit normal of the oval at angle th."""
    a, b = strap_e(th - 1e-3), strap_e(th + 1e-3); T = (b - a).normalized(); N = Vector((T.y, -T.x))
    return N if N.dot(strap_e(th)) >= 0 else -N

def arrive_off(th):
    """The returning strip rides over the strip's own start as it nears the loop (offset 0 → t)."""
    t = STRAP_T; d = th - LOOP_TH
    if d <= 0: return t
    k = max(0.0, 1 - d / 0.45); return t * k * k * (3 - 2 * k)

def strap_path():
    """(point, angle) along the strip centre line: start at the loop (its inner bar wrapped inside), past the pod, once
    round the wrist, back over its own start, through the loop, a fold over the loop's outer bar, and the tail running
    back on the outside: the hook-and-loop closure sits on the side opposite the sensors."""
    t = STRAP_T; pts = []; n = 420
    for k in range(n + 1):
        th = LOOP_TH + 0.065 - (2 * math.pi + OV + 0.065) * k / n   # starts past the inner bar, which it wraps
        off = arrive_off(th + 2 * math.pi) if k > n * 0.5 else 0.0
        pts.append(strap_e(th) + strap_n(th) * off)
    thF = LOOP_TH - OV; P0 = strap_e(thF) + strap_n(thF) * t; No = strap_n(thF)
    Tm = (strap_e(thF - 1e-3) - strap_e(thF + 1e-3)).normalized()       # direction of travel (decreasing angle)
    r = 0.0011                                            # soft U fold; the tail comes back over the strip, under the loop's outer bar
    for k in range(1, 16):
        ph = math.pi * k / 16
        pts.append(P0 + No * (r - r * math.cos(ph)) + Tm * (r * 1.25) * math.sin(ph))
    m = 160
    for k in range(m + 1):
        th = thF + (OV + math.radians(150)) * k / m
        k = max(0.0, 1 - (th - thF) / (OV + 0.35)); k = k * k * (3 - 2 * k)       # the tail settles onto the strip past the loop
        pts.append(strap_e(th) + strap_n(th) * (arrive_off(th) + t + (2 * r - t) * k))
    return pts

def build_strip():
    """The strip as one swept solid; its section has a flat body and corded (piped) edges."""
    t, h, z0 = STRAP_T, STRAP_H, STRAP_LIFT
    rp = 0.00085; phi0 = math.acos(min(1.0, (t / 2) / rp))
    prof = []                                             # (offset across the thickness, z)
    for k in range(10):                                    # top cord
        a = -phi0 + (math.pi + 2 * phi0) * k / 9; prof.append((rp * math.cos(a), z0 + h - rp + rp * math.sin(a)))
    for k in range(10):                                    # bottom cord
        a = math.pi - phi0 + (math.pi + 2 * phi0) * k / 9; prof.append((rp * math.cos(a), z0 + rp + rp * math.sin(a)))
    path = strap_path(); bm = bmesh.new(); secs = []
    for i, pnt in enumerate(path):
        a = path[max(i - 1, 0)]; b = path[min(i + 1, len(path) - 1)]
        T = (b - a).normalized(); N = Vector((T.y, -T.x))
        secs.append([bm.verts.new((pnt.x + N.x * o, pnt.y + N.y * o, z)) for o, z in prof])
    k = len(prof)
    for i in range(len(secs) - 1):
        A, B = secs[i], secs[i + 1]
        for q in range(k): bm.faces.new((A[q], A[(q + 1) % k], B[(q + 1) % k], B[q]))
    bm.faces.new(list(reversed(secs[0]))); bm.faces.new(secs[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return link('strip', bm, 'loop')

def build_pod():
    """Slim graphite pod on the inner side of the straight stretch, next to the loop: soft-cornered, a dark sensor
    window on the wrist face; its lower edge leaves the strip and is the flat charging face."""
    t = STRAP_T; x_out = STRAP_XF - t / 2
    hgt = STRAP_LIFT + STRAP_H - 0.0012
    pod = rbox('pod', POD_LEN, hgt, POD_T, 0.0042, 0.0007, 'modalu', sp=10, se=4)
    pod.rotation_euler = (math.pi / 2, 0, math.pi / 2)
    pod.location = (x_out - POD_T, 0.0005, hgt / 2)
    lens = rbox('lens', 0.011, 0.0065, 0.0003, 0.0028, 0.0001, 'lens', sp=8, se=1)
    lens.rotation_euler = (math.pi / 2, 0, -math.pi / 2)
    lens.location = (x_out - POD_T - 0.00002, 0.0005, STRAP_LIFT + STRAP_H * 0.5)
    return [pod, lens]

def build_loop():
    """Steel loop as a flat metal ribbon bent into a soft rectangle around the strip layers; its inner bar is wrapped
    inside the strip's start, so only the outer bar and the two arms show."""
    t, h, z0 = STRAP_T, STRAP_H, STRAP_LIFT
    c2 = strap_e(LOOP_TH); N2 = strap_n(LOOP_TH); T2 = Vector((-N2.y, N2.x))
    n_in, n_out = 0.0, 1.5 * t + 2 * 0.0011 + 0.0006 + BAR_T / 2
    z_lo, z_hi = z0 - 0.0003 - BAR_T / 2, z0 + h + 0.0003 + BAR_T / 2
    rc = 0.0014; path = []
    corners = [(n_out - rc, z_hi - rc, 0), (n_in + rc, z_hi - rc, 90), (n_in + rc, z_lo + rc, 180), (n_out - rc, z_lo + rc, 270)]
    for cx, cz, a0 in corners:
        for k in range(9):
            a = math.radians(a0 + 90 * k / 8); path.append((cx + rc * math.cos(a), cz + rc * math.sin(a)))
    sec = []; cr = 0.00035
    for qx, qy, a0 in ((BAR_W / 2 - cr, BAR_T / 2 - cr, 0), (-BAR_W / 2 + cr, BAR_T / 2 - cr, 90), (-BAR_W / 2 + cr, -BAR_T / 2 + cr, 180), (BAR_W / 2 - cr, -BAR_T / 2 + cr, 270)):
        for k in range(4):
            a = math.radians(a0 + 90 * k / 3); sec.append((qx + cr * math.cos(a), qy + cr * math.sin(a)))
    bm = bmesh.new(); rings = []; L = len(path)
    for i, (nn, zz) in enumerate(path):
        a = path[(i - 1) % L]; b = path[(i + 1) % L]
        dn, dz = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dn, dz); dn, dz = dn / ln, dz / ln
        pn, pz = -dz, dn                                      # in-plane normal of the ribbon's path
        ring = []
        for sw, sq in sec:
            v2 = c2 + N2 * (nn + pn * sq) + T2 * sw
            ring.append(bm.verts.new((v2.x, v2.y, zz + pz * sq)))
        rings.append(ring)
    k = len(sec)
    for i in range(L):
        A, B = rings[i], rings[(i + 1) % L]
        for q in range(k): bm.faces.new((A[q], A[(q + 1) % k], B[(q + 1) % k], B[q]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return link('steelloop', bm, 'steel')

def build_bracelet(z0=0.0):
    parts = [build_strip(), build_loop()] + build_pod()
    g = group('bracelet', parts); g.location.z = z0; g.rotation_euler = (0, 0, AP)
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
# Anatomical hands for the gesture drawings (owner, 2026-10-29): MPFB2's CC0 human, posed and cut out by
# hand_mpfb.py into deck/blender/hands/<pose>.obj. Frame: X along the fingers, Y towards the thumb, Z the back of the
# hand, the wrist at the origin, metres; hands.json holds the index and thumb tips. A subdivision smooths the low-poly
# base mesh, so Freestyle draws only its outline and real creases.
HANDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hands')
HAND_TIPS = json.load(open(os.path.join(HANDS, 'hands.json')))

def hand_mesh(pose):
    vs, fs = [], []
    for ln in open(os.path.join(HANDS, f'{pose}.obj')):
        if ln.startswith('v '): vs.append(tuple(map(float, ln.split()[1:])))
        elif ln.startswith('f '): fs.append([int(i) - 1 for i in ln.split()[1:]])
    return vs, fs

def build_hand(pose, R, t, name='hand'):
    """R: 3×3 world basis of the hand (columns = local X, Y, Z); t: world position of the wrist."""
    vs, fs = hand_mesh(pose)
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    ob = bpy.data.objects.new(name, me); col.objects.link(ob); me.materials.append(M('skin'))
    W = Matrix.Translation(t) @ R.to_4x4(); ob.matrix_world = W
    sub = ob.modifiers.new('smooth', 'SUBSURF'); sub.levels = sub.render_levels = 2
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    return [ob], {k: W @ Vector(HAND_TIPS[pose][k]) for k in ('index', 'thumb')}

def wrist_fit(pose):
    """Centre (y, z) and half-width / half-thickness of the wrist just behind the joint, in the hand frame."""
    vs, _ = hand_mesh(pose); sl = [(y, z) for x, y, z in vs if -0.03 < x < -0.008]
    ys, zs = [y for y, _ in sl], [z for _, z in sl]
    return (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2, (max(ys) - min(ys)) / 2, (max(zs) - min(zs)) / 2

def palm_z(pose):
    """Lowest point of the palm (local z), so a resting hand can sit on a surface."""
    vs, _ = hand_mesh(pose)
    return min(z for x, y, z in vs if 0.03 < x < 0.09)

def basis(x, y):
    x = Vector(x).normalized(); y = (Vector(y) - x * x.dot(Vector(y))).normalized(); z = x.cross(y)
    return Matrix((x, y, z)).transposed()

def pinch_hand(target, R):
    """Hand placed so that the pad between thumb and index tip lands on target."""
    m = (Vector(HAND_TIPS['pinch']['index']) + Vector(HAND_TIPS['pinch']['thumb'])) / 2
    return build_hand('pinch', R, Vector(target) - R @ m)

GRIP = (0.0277, 0.0030)          # the bracelet's pod side, turned to face +X by AP: where the fingers pinch it
PINCH_R = basis((-0.906, 0.0, -0.423), (0.0, -1.0, 0.0))   # from the right like the palm, index inside the band, thumb outside

def build_gesture(n):
    """01 take the bracelet off the base, 02 palm on the base (bracelet on the wrist), 03 put it back, 04 palm held 3 s."""
    base = build_base(with_time=True, time={1: '22:00', 2: '06:16', 3: '86%', 4: 'OFF'}[n])   # awake: the time is on; bracelet back: its charge
    if n in (2, 4):            # 02 a short tap in the morning, the hand just above the top; 04 the palm held 3 s (evening)
        F = Vector((-1, -1, 0)).normalized()          # along the diagonal that runs across the drawing: seen side-on
        R = basis(F, Vector((0, 0, 1)).cross(F))                                       # thumb to the left of the fingers
        lift = 0.018 if n == 2 else 0.0
        wrist = Vector((0.058, 0.058, TOP - palm_z('palm') + 0.0005 + lift))     # the heel of the palm on the right corner
        hand, tips = build_hand('palm', R, wrist)
        yc, zc, hw, ht = wrist_fit('palm')
        br = build_bracelet()                                                          # worn: the strap closed to the wrist
        br.scale = ((ht + 0.0022) / STRAP_B, (hw + 0.0022) / STRAP_A, 1)
        br.matrix_world = (Matrix.Translation(wrist + R @ Vector((-0.004, yc, zc))) @ Matrix.Rotation(math.atan2(-F.y, -F.x), 4, 'Z')
                           @ Matrix.Rotation(math.pi / 2, 4, 'Y') @ Matrix.Diagonal(br.scale.to_4d()))   # ring round the wrist, pod underneath
        return group('gesture', [base, br] + hand)
    z0 = TOP + (0.042 if n == 1 else 0.010)
    br = build_bracelet(z0)
    hand, tips = pinch_hand((GRIP[0], GRIP[1], z0 + STRAP_LIFT + STRAP_H - 0.004), PINCH_R)
    return group('gesture', [base, br] + hand)

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
        build_bracelet(); a = AP; fw = 0.055
        tgt = (0.024 * math.cos(a), 0.024 * math.sin(a), 0.006); pos = (0.024 * math.cos(a) * 4.2, 0.024 * math.sin(a) * 4.2, 0.035)
    elif view == 'pod_in':
        build_bracelet(); a = AP; fw = 0.06
        c = Vector((0.02 * math.cos(a), 0.02 * math.sin(a), 0.011))
        tgt = tuple(c); pos = tuple(c - Vector((math.cos(a), math.sin(a), 0)) * 0.16 + Vector((0, 0, 0.09)))
    elif view == 'pod_side':
        build_bracelet(); a = AP; fw = 0.06
        c = Vector((0.024 * math.cos(a), 0.024 * math.sin(a), 0.011)); tg = Vector((-math.sin(a), math.cos(a), 0))
        tgt = tuple(c); pos = tuple(c + tg * 0.2 + Vector((math.cos(a), math.sin(a), 0)) * 0.012)
    elif view == 'band':
        build_bracelet(); fw, tgt, pos = 0.13, (0, 0, 0.011), (0.6, -0.9, 0.55)
    elif view in ('left', 'right'):
        build_base(); fw = W / 0.62; tgt = (0, 0, TOP * 0.5); pos = (-1 if view == 'left' else 1, 0, TOP * 0.42)
    elif view == 'top_cable':
        build_base()
        boot = rbox('boot', 0.011, 0.016, 0.0062, 0.0005, 0.0003, 'plug', (0, W / 2 + 0.008, MID - 0.0031), sp=4, se=2)   # nearly sharp corners (owner)
        wn = boot.modifiers.new('wn', 'WEIGHTED_NORMAL'); wn.keep_sharp = True; wn.mode = 'FACE_AREA'   # flat faces, no diagonal shading
        cyl('usb', 0.0021, 0.5, 'cable', (0, W / 2 + 0.016 + 0.25, MID), axis='Y', seg=48)
        fw = 0.32; tgt = (0, 0.026, TOP / 2); pos = (0, 0.0261, 1)   # a stretch of braided cable shows before the frame cuts it
    elif view == 'time':
        build_base(with_time=True); fw = 0.11; tgt = (-0.004, -W / 2 + 0.01, MID); pos = (-0.004 + 0.55, -W / 2 - 1.0, MID + 0.32)   # 3/4 on the time
    elif view == 'ports':
        build_base(); fw = 0.11; tgt = (-0.018, W / 2 - 0.01, MID); pos = (-0.018 - 0.55, W / 2 + 1.0, MID + 0.32)   # 3/4 on the back marks
    elif view == 'led':
        build_base(); fw = 0.11; tgt = (0.03, -W / 2 + 0.01, MID); pos = (0.03 + 0.55, -W / 2 - 1.0, MID + 0.32)   # 3/4 on the LED: the alarm still reads
    elif view == 'strip':
        build_base(); fw = W / 0.5; tgt = (0, 0, 0.004); pos = (0.55, -0.75, -0.17)
    elif view in ('persp', 'lit', 'persp_back', 'persp_band'):
        build_base(with_time=(view == 'lit')); fw, tgt = W / 0.55, (0, 0, TOP * 0.42)
        if view == 'persp_band': build_bracelet(TOP); fw, tgt = W / 0.52, (0, 0, TOP * 0.75)
        pos = (-0.62, 0.95, 0.24) if view == 'persp_back' else (0.62, -0.95, 0.24)
    else:
        build_base()
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
    if view in ('persp', 'lit', 'band', 'persp_back', 'persp_band', 'foot', 'pod_side', 'pod_in'): area('front', tuple(Vector(cam.location) * 0.8 + Vector((-0.3, 0, 0.2))), tgt, 1.4, 40)
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
    boot = rbox('boot', 0.011, 0.016, 0.0062, 0.0005, 0.0003, 'plug', (0, W / 2 + 0.008, MID - 0.0031), sp=4, se=2)   # nearly sharp corners (owner)
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
    scene.render.filepath = os.path.join(OUT, f'aurawake-{SHOT}{"-" + STATE if STATE else ""}{"-plastic" if PLASTIC else ""}{"-coarse" if COARSE else ""}{"-seg" if SEGS else ""}{"-grid" if GRIDT else ""}{"-preview" if PREVIEW else ""}.png')
    bpy.ops.render.render(write_still=True)

# ---------------------------------------------------------------------------------------------------------------
# Technical drawings: true isometric ortho camera, flat fills, Freestyle lines (outline heavier than inner lines).
ISO = (math.radians(54.7356), 0.0, math.radians(45))
ISO_UNDER = (math.radians(180 - 54.7356), 0.0, math.radians(135))   # from below, behind: back, right side and underneath
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
    cam = bpy.data.objects.new('iso', cd); col.objects.link(cam); scene.camera = cam

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
        'g1': (lambda: build_gesture(1), 560, {'top': (0, 0, TOP)}),
        'g2': (lambda: build_gesture(2), 560, {'top': (0, 0, TOP)}),
        'g3': (lambda: build_gesture(3), 560, {'top': (0, 0, TOP)}),
        'g4': (lambda: build_gesture(4), 560, {'top': (0, 0, TOP)}),
        'base_under': (build_base, 300, {'under': (0.0, 0.0, 0.0), 'back': (0.0, W / 2, MID), 'under_exit': (-W / 2, -W / 2, PL), 'back_exit': (0.0, W / 2, TOP)}, ISO_UNDER),
    }
    if SHOT: items = {SHOT: items[SHOT]}                 # one drawing only: merged into the existing anchors
    path = os.path.join(OUT, 'anchors.json')
    anchors = json.load(open(path)) if SHOT and os.path.exists(path) else {}
    for name, (fn, size, pts, *rot) in items.items():
        cam.rotation_euler = rot[0] if rot else ISO; bpy.context.view_layer.update()
        R = cam.matrix_world.to_3x3(); right, up, back = R.col[0], R.col[1], R.col[2]
        for o in list(col.objects):
            if o.type != 'CAMERA': bpy.data.objects.remove(o, do_unlink=True)
        g = fn(); bpy.context.view_layer.update()
        fit = [o for o in g.children_recursive if (o.type == 'MESH' or o.name.startswith('band')) and not o.name.startswith('hand')]
        if name.startswith('g'): fit = [o for o in fit if o.name == 'body']     # gestures: the base sits in the same place in all three
        cs = [o.matrix_world @ Vector(c) for o in fit for c in o.bound_box]
        xs = [c.dot(right) for c in cs]; ys = [c.dot(up) for c in cs]
        span = max(max(xs) - min(xs), max(ys) - min(ys)) * (1.16 if not name.startswith('g') else 1.0)
        if name.startswith('g'): span = 0.30                    # gestures: one scale for all three, the hand runs off the frame
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        if name.startswith('g'): cx, cy = cx + 0.015, cy + 0.04           # room for the hand above and to the right
        cam.location = right * cx + up * cy + back * 2.0
        cd.ortho_scale = span; cd.clip_end = 10
        px = round(size * SS); scene.render.resolution_x = scene.render.resolution_y = px
        freestyle(2.6, 5.2)
        bpy.context.view_layer.update()
        def proj(p):
            v = world_to_camera_view(scene, cam, Vector(p)); return [round(v.x * size, 1), round((1 - v.y) * size, 1)]
        anchors[name] = {'size': size, 'k': round(size / span, 1), 'ground': proj((0, 0, 0)), 'points': {k: proj(p) for k, p in pts.items()}}
        scene.render.filepath = os.path.join(OUT, f'iso-{name}.png')
        bpy.ops.render.render(write_still=True)
    with open(path, 'w') as f: json.dump(anchors, f, indent=1)

real() if MODE == 'real' else line()
