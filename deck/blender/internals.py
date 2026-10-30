# AuraWake base, inside (owner, 2026-10-30: "come se dovessi farla funzionare … come apparirebbe smontata nei minimi
# dettagli"). Every part is a catalogue part at its datasheet size, placed where it sits in the 120 × 120 × 45 mm
# enclosure; build_exploded() pulls the groups apart (and draws the cables between them) for the exploded views.
# Acoustics (owner, 2026-10-30): two 36 mm full-range drivers firing left and right + a 40 × 60 mm passive radiator
# behind the back grille; the whole sealed interior (≈ 300 cm³) is their back volume. Loaded by aura.py with exec(),
# so it shares its helpers (rbox, cyl, link, group, label, M, W, H, PL, TOP, MID, BTN_X, BTN_HOLE …). Metres.
import random
WALL = 0.002                       # shell wall and top thickness (PC/ABS, satin)
IN = W - 2 * WALL                  # 116 mm inside
FLOOR = PL + WALL                  # top of the bottom plate, 4.2 mm
CEIL = TOP - WALL                  # underside of the top, 43.0 mm
PCB_T = 0.0010                     # 4-layer board, 1.0 mm
PCB_Z = MID - 0.0016 - PCB_T       # main board: its top 1.6 mm under the USB-C centre line (mid-mount receptacle)
ZT = PCB_Z + PCB_T                 # top of the main board
PIN_Y = -W / 2 + 0.020             # the row of charging pins
BOM = []                           # (key, part, maker / code, notes) for the parts list
LINE = MODE != 'real'

def part(key, text, code, note=''):
    if not any(b[0] == key for b in BOM): BOM.append((key, text, code, note))

# materials the line drawing needs as flat tones (real mode gets real ones in real_mats)
if LINE:
    for k, v in {'pcb': 0.48, 'chip': 0.22, 'shield': 0.84, 'speaker': 0.30, 'cone': 0.62, 'battery': 0.80, 'copper': 0.74,
                 'pmma': 0.97, 'chassis': 0.90, 'magnet': 0.56, 'screw': 0.45, 'led': 0.98, 'mlcc': 0.72, 'res': 0.20, 'term': 0.88,
                 'kapton': 0.70, 'wire_r': 0.55, 'wire_k': 0.20, 'wire_w': 0.95, 'jst': 0.96, 'foam': 0.75, 'brass': 0.70,
                 'surround': 0.25, 'nickel': 0.86, 'silk': 0.95, 'etch': 0.60, 'label': 0.96, 'gold': 0.70, 'alcap': 0.82}.items():
        MATS.setdefault(k, toon(k, grey(v)))

# ---------------------------------------------------------------------------------------------------------------
# geometry helpers
def box(name, w, d, h, x, y, z, mat, r=0.0):
    """A component as a box: w (x) × d (y) × h (z), its base centre at (x, y, z)."""
    return rbox(name, w, d, h, r, min(r, h / 3) if r else 0.0, mat, (x, y, z), sp=4 if r else 1, se=1)

def add_box(bm, x, y, z, w, d, h):
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((x, y, z + h / 2)) @ Matrix.Diagonal((w, d, h, 1.0)))

def annulus(name, r_in, r_out, h, mat, z, n=96, loc=(0, 0)):
    """A flat ring (board, gasket, light guide), its base at z."""
    bm = bmesh.new(); vs = []
    for i in range(n):
        a = 2 * math.pi * i / n; c, sn = math.cos(a), math.sin(a)
        vs.append([bm.verts.new((r * c, r * sn, zz)) for r, zz in ((r_in, 0), (r_out, 0), (r_out, h), (r_in, h))])
    for i in range(n):
        A, B = vs[i], vs[(i + 1) % n]
        for k in range(4): bm.faces.new((A[k], B[k], B[(k + 1) % 4], A[(k + 1) % 4]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return link(name, bm, mat, (loc[0], loc[1], z))

def torus(name, R, r, mat, z=0.0, n=96, m=16, half=False):
    """A ring of round section (a speaker's rubber surround); half = only the outer half of the section, facing +z."""
    bm = bmesh.new(); rings = []; mm = m // 2 + 1 if half else m
    for i in range(n):
        a = 2 * math.pi * i / n; ring = []
        for j in range(mm):
            b = math.pi * j / (mm - 1) if half else 2 * math.pi * j / m
            rr = R + r * math.cos(b); ring.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), z + r * math.sin(b))))
        rings.append(ring)
    for i in range(n):
        A, B = rings[i], rings[(i + 1) % n]
        for j in range(mm - 1 if half else m):
            bm.faces.new((A[j], A[(j + 1) % mm], B[(j + 1) % mm], B[j]))
    ob = link(name, bm, mat); return ob

def cone_shell(name, r0, r1, depth, mat, z=0.0, seg=96):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=False, segments=seg, radius1=r0, radius2=r1, depth=depth, matrix=Matrix.Translation((0, 0, z + depth / 2)))
    ob = link(name, bm, mat); sol = ob.modifiers.new('t', 'SOLIDIFY'); sol.thickness = 0.0003; return ob

def wires(name, pts, colours, r=0.00045, gap=0.0011):
    """A small bundle of wires along the same path, side by side (red/black, or white/red/black)."""
    obs = []; n = len(colours)
    for i, c in enumerate(colours):
        off = (i - (n - 1) / 2) * gap
        obs.append(curve(f'{name}{i}', [(p[0] + off, p[1], p[2]) for p in pts], r, c))
    return obs

def flex(name, pts, width, mat='kapton'):
    """A flat flex cable along a path (bezier, extruded sideways)."""
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.extrude = width / 2; cu.twist_mode = 'Z_UP'
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts): bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu); col.objects.link(ob); cu.materials.append(M(mat)); return ob

def tail_flex(name, x, y, z_top, z_bot, w=0.005, t=0.00012, rb=0.0015):
    """The electrode's tail: flat, w wide along x, hanging straight down from z_top to z_bot at (x, y), with a
    rounded 90° bend into the electrode at the top and a short foot onto the spring contact at the bottom."""
    bm = bmesh.new()
    add_box(bm, x, y + rb + 0.004, z_top - t, w, 0.008, t)                              # under the electrode, out past its edge
    for k in range(6):                                                                  # the bend, in 6 steps
        a0, a1 = math.pi / 2 * k / 6, math.pi / 2 * (k + 1) / 6
        yy = y + rb - rb * math.sin((a0 + a1) / 2); zz = z_top - rb + rb * math.cos((a0 + a1) / 2)
        add_box(bm, x, yy, zz - t / 2, w, max(t, rb * (math.sin(a1) - math.sin(a0))) + t, max(t, rb * (math.cos(a0) - math.cos(a1))) + t)
    add_box(bm, x, y, z_bot + 0.0015, w, t, z_top - rb - z_bot - 0.0015)                 # the straight drop
    add_box(bm, x, y + 0.00175, z_bot, w, 0.0035, t)                                     # the foot onto the spring
    return link(name, bm, 'kapton', smooth=False)

def screw(name, x, y, z, r, length, mat='screw', up=True):
    """Pan-head Phillips screw: head on top (up) or below, a cross recess, the thread as a plain shank."""
    s = 1 if up else -1; obs = []
    obs.append(cyl(f'{name}_shank', r, length, mat, (x, y, z - s * length / 2), seg=20))
    obs.append(cyl(f'{name}_head', r * 1.9, r * 1.1, mat, (x, y, z + s * r * 0.55), seg=32))
    for a in (0, math.pi / 2):
        b = box(f'{name}_x{a:.1f}', r * 1.8, r * 0.35, r * 0.4, x, y, z + (r * 1.1 - r * 0.38 if up else -r * 1.1 - 0.00002), 'chip')
        b.rotation_euler.z = a; obs.append(b)
    return obs

class Scatter:
    """Passive parts packed round the ICs and in the free board area, kept out of every placed part."""
    def __init__(self, rects, keep):
        self.rects, self.keep = rects, keep
    def free(self, x, y, w, d):
        if not any(x0 + w / 2 <= x <= x1 - w / 2 and y0 + d / 2 <= y <= y1 - d / 2 for x0, y0, x1, y1 in self.rects): return False
        return not any(abs(x - kx) < (kw + w) / 2 and abs(y - ky) < (kd + d) / 2 for kx, ky, kw, kd in self.keep)
    def take(self, x, y, w, d, pad=0.0003):
        self.keep.append((x, y, w + pad * 2, d + pad * 2))

def passives(prefix, sc, z, seeds, n_fill, rng):
    """0402 / 0603 MLCCs (tan body) and resistors (black top) with tinned ends, as three meshes."""
    bodies_c, bodies_r, terms = bmesh.new(), bmesh.new(), bmesh.new(); count = 0
    def put(x, y, rot, big=False):
        nonlocal count
        L, Wd, Hh = (0.0016, 0.0008, 0.0008) if big else (0.0010, 0.0005, 0.0005)
        w, d = (L, Wd) if rot == 0 else (Wd, L)
        if not sc.free(x, y, w + 0.0003, d + 0.0003): return False
        sc.take(x, y, w, d)
        body = bodies_r if rng.random() < 0.35 else bodies_c
        tl = L * 0.22
        if rot == 0:
            add_box(body, x, y, z, L - 2 * tl, Wd, Hh)
            for sx in (-1, 1): add_box(terms, x + sx * (L / 2 - tl / 2), y, z, tl, Wd, Hh)
        else:
            add_box(body, x, y, z, Wd, L - 2 * tl, Hh)
            for sy in (-1, 1): add_box(terms, x, y + sy * (L / 2 - tl / 2), z, Wd, tl, Hh)
        count += 1; return True
    for (cx, cy, w, d) in seeds:                     # decoupling round every IC: a ring of parts 0.8 mm off its edge
        for side in range(4):
            n = int((w if side % 2 == 0 else d) / 0.0016)
            for k in range(n):
                t = (k + 0.5) / n - 0.5
                if side == 0: put(cx + t * w, cy + d / 2 + 0.0011, 1)
                elif side == 1: put(cx + w / 2 + 0.0011, cy + t * d, 0)
                elif side == 2: put(cx + t * w, cy - d / 2 - 0.0011, 1)
                else: put(cx - w / 2 - 0.0011, cy + t * d, 0)
    tries = 0
    while count < n_fill and tries < n_fill * 40:   # the rest of the board: loose rows, as a router leaves them
        tries += 1
        x0, y0, x1, y1 = rng.choice(sc.rects)
        x = rng.uniform(x0 + 0.002, x1 - 0.002); y = rng.uniform(y0 + 0.002, y1 - 0.002); rot = rng.choice((0, 1))
        for k in range(rng.randint(1, 5)):
            put(x + (k * 0.0019 if rot == 1 else 0), y + (k * 0.0019 if rot == 0 else 0), rot, big=rng.random() < 0.12)
    return [link(f'{prefix}_mlcc', bodies_c, 'mlcc', smooth=False), link(f'{prefix}_res', bodies_r, 'res', smooth=False),
            link(f'{prefix}_term', terms, 'term', smooth=False)]

# ---------------------------------------------------------------------------------------------------------------
# the parts
def shell():
    part('shell', 'Enclosure: top and four walls in one piece', 'PC/ABS, satin, 2.0 mm walls',
         'grilles left, right and back; 3 pin holes on top; front: only the LED hole, the time window of laser micro-holes (light sensor and mic behind it)')
    outer = rbox('shell', W, W, H, EDGE_P, EDGE_T, 'body', (0, 0, PL), sp=4, se=2)
    if MODE == 'real':                                   # the same openings as the finished base
        cut(outer, stadium_bm(0.0084, 0.0026, 0.012), (0, W / 2, MID), 'rubber')
        cut(outer, cutter_bm([(BTN_X, 0, BTN_HOLE)], 0.002), (0, W / 2, MID), 'rubber')
        cut(outer, holes_bm(), (0, 0, 0), 'cavity')
    cutter = rbox('shell_in', IN, IN, H - WALL + 0.001, 0.001, 0.0, 'body', (0, 0, PL - 0.001), sp=2)
    boolean_diff(outer, cutter); holes_line = []
    for name, x, y, z, r, ax in (('ph0', -0.004, PIN_Y, TOP - 0.001, 0.00095, 'Z'), ('ph1', 0.0, PIN_Y, TOP - 0.001, 0.00095, 'Z'),
                                 ('ph2', 0.004, PIN_Y, TOP - 0.001, 0.00095, 'Z'), ('led_h', 0.036, -W / 2 + 0.001, MID, 0.00085, 'Y')):
        if LINE:                                         # the drawing: a dark disc reads as the hole, no boolean seams
            d = cyl(name, r, 0.0002, 'chip', (x, y, TOP + 0.00005) if ax == 'Z' else (x, -W / 2 - 0.00005, z), axis=ax, seg=32)
            holes_line.append(d)
        else:
            c = cyl(name, r, 0.006, 'cavity', (x, y, z), axis=ax, seg=32); boolean_diff(outer, c)
    return [outer] + holes_line

def top_inside():
    """Under the top: the touch electrode with its flex tail, the pin block and the two centring magnets."""
    part('touch', 'Touch electrode under the top (palm)', 'copper on 0.1 mm polyimide, 100 × 76 mm, flex tail to a spring contact',
         'read by the ESP32-S3 capacitive touch; a 3 mm keep-out round the pins and magnets')
    part('pins', 'Bracelet charging contacts, 3 positions, 4 mm pitch', 'Mill-Max 0906 spring pins on a carrier board, gold',
         'through 3 holes in the top, sealed with a silicone gasket; powered only when the bracelet ID answers')
    part('magnets', 'Centring magnets ×2', 'N52 NdFeB disc Ø6 × 2 mm in steel cups', 'pull the bracelet’s flat edge onto the pins')
    obs = []
    obs.append(box('kapton_sheet', 0.102, 0.078, 0.00008, 0, 0.012, CEIL - 0.00018, 'kapton'))
    obs.append(box('electrode', 0.100, 0.076, 0.00004, 0, 0.012, CEIL - 0.0001 - 0.00004, 'copper'))
    obs.append(box('pin_board', 0.024, 0.009, 0.0008, 0, PIN_Y, CEIL - 0.0050, 'pcb'))
    obs.append(box('pin_jst', 0.0058, 0.0035, 0.0029, 0.0085, PIN_Y, CEIL - 0.0050 - 0.0029, 'jst'))
    obs.append(box('gasket', 0.016, 0.005, 0.0012, 0, PIN_Y, CEIL - 0.0012, 'rubber', 0.001))
    for i in (-1, 0, 1):
        obs.append(cyl(f'pin_barrel{i}', 0.0009, 0.0034, 'gold', (i * 0.004, PIN_Y, CEIL - 0.0042 + 0.0017), seg=24))
        obs.append(cyl(f'pin_tip{i}', 0.00075, 0.0026, 'gold', (i * 0.004, PIN_Y, CEIL + 0.0007), seg=24))
    for sx in (-1, 1):
        obs.append(cyl(f'magnet_cup{sx}', 0.0036, 0.0026, 'nickel', (sx * 0.013, PIN_Y, CEIL - 0.0013), seg=32))
        obs.append(cyl(f'magnet{sx}', 0.003, 0.002, 'magnet', (sx * 0.013, PIN_Y, CEIL - 0.0010), seg=32))
    return obs

def display():
    """Behind the front wall: the dot matrix for the time, its cell baffle and diffuser, the front LED, light sensor, mic."""
    part('matrix', 'Time display: 0402 warm-white LEDs on a 1.33 mm grid', '351 positions, driver Lumissil IS31FL3741 (I²C)',
         'black cell baffle + diffuser film, bonded behind ~0.1 mm laser micro-holes in a 0.5 mm thinned window of the front wall')
    part('status', 'Front status LED (day): RGB with a light pipe', 'Everlight 99-235 RGB + PC light pipe Ø1.7 mm', '')
    part('als', 'Ambient light sensor', 'Vishay VEML7700 (I²C)', 'behind the right end of the micro-hole window')
    part('mic', 'Microphone (snoring, noise; never recorded)', 'Knowles SPH0645LM4H, I²S MEMS', 'behind the micro-hole window, sealed to it by a mesh gasket')
    y = -IN / 2 + 0.0004; obs = []                       # the front face of the stack touches the wall
    pb = y + 0.0042                                      # the board's front face
    obs.append(box('disp_pcb', 0.068, 0.0010, 0.028, -0.002, pb + 0.0005, MID - 0.014, 'pcb'))
    pitch = PU / 3; x0 = -0.006; cols, rows = 25, 7
    gw, gh = cols * pitch, rows * pitch
    bf = bmesh.new()                                     # the baffle: a black grid of 0.2 mm walls, one cell per LED
    for c in range(cols + 1): add_box(bf, x0 + (c - cols / 2) * pitch, y + 0.0020, MID - gh / 2, 0.0002, 0.0032, gh)
    for r in range(rows + 1): add_box(bf, x0, y + 0.0020, MID - gh / 2 + r * pitch - 0.0001, gw, 0.0032, 0.0002)
    add_box(bf, x0, y + 0.0020, MID - gh / 2 - 0.0012, gw + 0.003, 0.0032, 0.0012)
    add_box(bf, x0, y + 0.0020, MID + gh / 2, gw + 0.003, 0.0032, 0.0012)
    obs.append(link('baffle', bf, 'chip', smooth=False))
    obs.append(box('diffuser', gw + 0.003, 0.0002, gh + 0.0024, x0, y + 0.0002, MID - gh / 2 - 0.0012, 'pmma'))
    lb, lp = bmesh.new(), bmesh.new()
    for c in range(cols):
        for r in range(rows):
            cx, cz = x0 + (c - (cols - 1) / 2) * pitch, MID + ((rows - 1) / 2 - r) * pitch
            add_box(lb, cx, pb - 0.00025, cz - 0.00025, 0.0010, 0.0005, 0.0005)
            add_box(lp, cx, pb - 0.00052, cz - 0.00018, 0.0006, 0.00004, 0.00036)
    obs.append(link('leds', lb, 'led', smooth=False)); obs.append(link('led_phos', lp, 'alcap', smooth=False))
    obs.append(box('drv', 0.006, 0.0008, 0.006, 0.022, pb - 0.0004, MID - 0.010, 'chip'))
    obs.append(cyl('lightpipe', 0.00085, 0.0040, 'pmma', (0.036, y + 0.0020, MID), axis='Y', seg=24))
    obs.append(box('rgb', 0.0016, 0.0006, 0.0016, 0.036, pb - 0.0003, MID - 0.0008, 'led'))
    xs = x0 + gw / 2 + 0.0035                            # right of the matrix, still behind the micro-hole window
    obs.append(box('als_chip', 0.0068, 0.0009, 0.0021, xs, pb - 0.00045, MID + 0.0008, 'chip'))
    obs.append(box('mic_chip', 0.0035, 0.0010, 0.0026, xs, pb - 0.0005, MID - 0.0042, 'shield'))
    obs.append(box('mic_mesh', 0.0040, 0.0020, 0.0032, xs, y + 0.0012, MID - 0.0045, 'foam'))
    obs.append(flex('fpc_disp', [(-0.002, pb + 0.001, MID - 0.013), (-0.002, pb + 0.006, MID - 0.016), (-0.002, -0.046, ZT + 0.0012)], 0.010))
    return obs

def main_board():
    part('pcb', 'Main board, 4 layers, 1.0 mm, black solder mask, ENIG', 'FR-4, 64 × 88 mm + a 48 × 12 mm tab for USB-C and button',
         'between the drivers; the radiator takes the other half of the back')
    part('s3', 'Wi-Fi + BLE: the brain', 'Espressif ESP32-S3-WROOM-1-N16R8', 'routines, ramps, Matter controller, app link, touch')
    part('h2', 'Thread / Matter radio (border router)', 'Espressif ESP32-H2-MINI-1', 'talks to lamp, shutters, diffuser')
    part('amp', 'Audio amplifiers ×2, 3.2 W class D', 'Analog Devices MAX98357A (I²S)', 'one per driver')
    part('pd', 'USB-C power: asks the charger for 5 V 3 A', 'ST STUSB4500 PD sink', '15 W in')
    part('chg', 'Backup battery charger + power path', 'TI BQ24074', 'runs everything from USB, tops up the cell')
    part('buck', '3.3 V regulator', 'TI TPS62133 buck, 3 A, with a 1 µH shielded inductor', '')
    part('gauge', 'Battery fuel gauge', 'Analog Devices MAX17048', '')
    part('rtc', 'Real-time clock on the battery', 'NXP PCF85063A + 32.768 kHz crystal', 'keeps 06:30 through a power cut')
    part('lsw', 'Bracelet pin power switch, current-limited', 'TI TPS2553 (300 mA limit)', 'on only after the ID line answers')
    part('usbc', 'USB-C receptacle, mid-mount, 16 pins, sealed', 'GCT USB4125 (IPX7 gasket)', 'keeps the acoustic volume closed')
    part('btn', 'Pairing button (sealed tactile switch + cap)', 'C&K KSC series, IP67', 'behind the round cap at the back')
    part('conn', 'Board connectors', 'JST SH 1.0 mm (speakers, pins, ring), JST PH 2.0 mm (cell), FPC ZIF 0.5 mm (display)', '')
    z = PCB_Z; obs = []; rng = random.Random(7)
    obs.append(box('main_pcb', 0.064, 0.088, PCB_T, 0, -0.002, z, 'pcb_main' if not LINE else 'pcb'))
    obs.append(box('pcb_tab', 0.048, 0.0125, PCB_T, -0.018, 0.04825, z, 'pcb_main' if not LINE else 'pcb'))
    # parts: (name, w, d, h, x, y, mat, designator)
    P = [('s3_mod', 0.018, 0.0255, 0.0024, -0.020, -0.03325, 'pcb', 'U1'), ('h2_mod', 0.0132, 0.0166, 0.0016, 0.018, -0.0377, 'pcb', 'U2'),
         ('amp_l', 0.003, 0.003, 0.0008, -0.024, 0.000, 'chip', 'U3'), ('amp_r', 0.003, 0.003, 0.0008, 0.024, 0.000, 'chip', 'U4'),
         ('pd_ic', 0.004, 0.004, 0.0008, -0.012, 0.0465, 'chip', 'U5'), ('chg_ic', 0.003, 0.004, 0.0008, 0.010, 0.028, 'chip', 'U6'),
         ('buck_ic', 0.003, 0.003, 0.0008, -0.010, 0.026, 'chip', 'U7'), ('gauge_ic', 0.002, 0.002, 0.0006, 0.018, 0.024, 'chip', 'U8'),
         ('rtc_ic', 0.003, 0.003, 0.0008, -0.022, 0.010, 'chip', 'U9'), ('lsw_ic', 0.002, 0.003, 0.0010, 0.006, -0.026, 'chip', 'U10'),
         ('drv_esd', 0.0016, 0.0010, 0.0006, 0.004, 0.0465, 'chip', 'D1'), ('xtal', 0.0032, 0.0015, 0.0008, -0.022, 0.0145, 'shield', 'Y1'),
         ('inductor', 0.004, 0.004, 0.0020, -0.017, 0.026, 'chip', 'L1'), ('cbulk1', 0.0035, 0.0028, 0.0019, -0.004, 0.034, 'chip', 'C1'),
         ('cbulk2', 0.0035, 0.0028, 0.0019, 0.020, 0.034, 'chip', 'C2'),
         ('j_disp', 0.014, 0.0045, 0.0012, -0.002, -0.0425, 'chip', 'J2'), ('j_pins', 0.0058, 0.0042, 0.0029, 0.0, -0.030, 'jst', 'J3'),
         ('j_spk_l', 0.0058, 0.0042, 0.0029, -0.028, 0.008, 'jst', 'J4'), ('j_spk_r', 0.0058, 0.0042, 0.0029, 0.028, 0.008, 'jst', 'J5'),
         ('j_batt', 0.0080, 0.0045, 0.0060, 0.022, 0.0395, 'jst', 'J6'), ('j_ring', 0.0068, 0.0042, 0.0029, -0.026, 0.034, 'jst', 'J7'),
         ('touch_spring', 0.0020, 0.0030, 0.0025, 0.026, -0.024, 'gold', 'J8')]
    keep = [(x, y, w + 0.0012, d + 0.0012) for _, w, d, h, x, y, _, _ in P]
    keep += [(-0.020, -0.043, 0.018, 0.006), (0.018, -0.043, 0.0132, 0.006)]                       # antenna keep-outs
    keep += [(x, y, 0.0056, 0.0056) for x in (-0.02, 0.02) for y in (-0.02, 0.02)]                  # mounting holes
    keep += [(0.0, 0.0505, 0.0110, 0.0080), (BTN_X, 0.0505, 0.0070, 0.0060), (0.012, 0.037, 0.006, 0.006)]   # USB-C, button, can
    for name, w, d, h, x, y, mat, ref in P:
        obs.append(box(name, w, d, h, x, y, ZT, mat, 0.0002 if mat == 'chip' and h > 0.0015 else 0.0))
    # modules: shield cans, pads, printed antennas, laser marking
    for nm, x, y, w, d, h in (('s3', -0.020, -0.03325, 0.018, 0.0255, 0.0024), ('h2', 0.018, -0.0377, 0.0132, 0.0166, 0.0016)):
        cw, cd = w - 0.0016, d - 0.0075
        obs.append(box(f'{nm}_can', cw, cd, 0.0008, x, y + (d - cd) / 2 - 0.0008, ZT + h, 'shield'))
        ant = bmesh.new(); ya = y - d / 2 + 0.0008; top = ZT + h
        for k in range(8): add_box(ant, x - w / 2 + 0.0025 + k * (w - 0.005) / 7, ya + 0.002, top, 0.0005, 0.0038, 0.00003)
        for k in range(7): add_box(ant, x - w / 2 + 0.0025 + (k + 0.5) * (w - 0.005) / 7, ya + (0.0039 if k % 2 == 0 else 0.0001), top, (w - 0.005) / 7 + 0.0005, 0.0005, 0.00003)
        obs.append(link(f'{nm}_ant', ant, 'gold', smooth=False))
        if not LINE:
            obs.append(label('ESP32-S3-WROOM-1' if nm == 's3' else 'ESP32-H2-MINI-1', 0.0011 if nm == 's3' else 0.00085,
                             (x, y + (d - cd) / 2 - 0.0008, ZT + h + 0.00081), (0, 0, 0), 'etch'))
            obs.append(label('N16R8  FCC ID 2AC7Z' if nm == 's3' else 'H4  CE', 0.0007, (x, y + (d - cd) / 2 - 0.0035, ZT + h + 0.00081), (0, 0, 0), 'etch'))
    # USB-C receptacle (mid-mount: through the board), sealed, and the button on the tab
    obs.append(box('usbc_rx', 0.0089, 0.0073, 0.0032, 0, W / 2 - WALL - 0.0036 - 0.0004, z - 0.0011, 'shield', 0.0012))
    obs.append(box('usbc_seal', 0.0095, 0.0010, 0.0038, 0, W / 2 - WALL - 0.0005, z - 0.0014, 'rubber', 0.0012))
    obs.append(box('btn_sw', 0.0062, 0.0062, 0.0035, BTN_X, W / 2 - WALL - 0.0038, ZT, 'chip', 0.0005))
    obs.append(cyl('btn_cap', 0.0047, 0.0026, 'shell', (BTN_X, W / 2 - WALL - 0.0013, MID), axis='Y', seg=48))
    # electrolytic can, test points, mounting holes, silkscreen
    obs.append(cyl('ecap', 0.0025, 0.0054, 'alcap', (0.012, 0.037, ZT + 0.0027), seg=32))
    obs.append(cyl('ecap_base', 0.0026, 0.0010, 'chip', (0.012, 0.037, ZT + 0.0005), seg=32))
    tp = bmesh.new(); vias = bmesh.new()
    for i in range(18):
        tx, ty = rng.uniform(-0.03, 0.03), rng.uniform(-0.02, 0.04)
        bmesh.ops.create_cone(tp, cap_ends=True, segments=16, radius1=0.0005, radius2=0.0005, depth=0.00004, matrix=Matrix.Translation((tx, ty, ZT + 0.00002)))
    for x in (-0.02, 0.02):
        for y in (-0.02, 0.02):
            obs.append(annulus(f'mh{x}{y}', 0.00125, 0.0024, 0.00004, 'gold', ZT, loc=(x, y)))
    obs.append(link('testpoints', tp, 'gold', smooth=False))
    sk = bmesh.new()
    for name, w, d, h, x, y, mat, ref in P:              # white outlines round the parts and the designators
        if w * d < 0.000012: continue
        for (bx, by, bw, bd) in ((x, y + d / 2 + 0.0005, w + 0.0012, 0.00015), (x, y - d / 2 - 0.0005, w + 0.0012, 0.00015),
                                 (x + w / 2 + 0.0005, y, 0.00015, d + 0.0012), (x - w / 2 - 0.0005, y, 0.00015, d + 0.0012)):
            add_box(sk, bx, by, ZT, bw, bd, 0.00002)
    obs.append(link('silk_outlines', sk, 'silk', smooth=False))
    if not LINE:
        for name, w, d, h, x, y, mat, ref in P:
            obs.append(label(ref, 0.0009, (x - w / 2 - 0.0018, y + d / 2 + 0.0012, ZT + 0.00003), (0, 0, 0), 'silk'))
        obs.append(label('AuraWake AW1  rev C  2026-10', 0.0013, (0.0, -0.016, ZT + 0.00003), (0, 0, 0), 'silk'))
        obs.append(label('USB-C', 0.0009, (0.0, 0.0445, ZT + 0.00003), (0, 0, 0), 'silk'))
    rects = [(-0.032, -0.046, 0.032, 0.042), (-0.042, 0.042, 0.006, 0.0545)]
    seeds = [(x, y, w, d) for name, w, d, h, x, y, mat, ref in P if mat == 'chip' and name not in ('cbulk1', 'cbulk2', 'j_disp', 'drv_esd')]
    obs += passives('main', Scatter(rects, keep), ZT, seeds, 330, rng)
    return obs

def chassis():
    part('chassis', 'Inner chassis: three sealed baffles + board bosses', 'PC-GF10, one moulding, brass M2 inserts',
         'round openings for the drivers left and right, an oval one at the back for the radiator; foam gaskets seal them to the walls')
    obs = []; h = CEIL - FLOOR - 0.002
    for sx in (-1, 1):                                   # side baffles with the driver openings
        x = sx * (IN / 2 - 0.0008 - 0.0008)
        wall = rbox(f'baffle_side{sx}', 0.0016, 0.096, h, 0.002, 0.0004, 'chassis', (x, -0.004, FLOOR + 0.001), sp=4, se=1)
        c = cyl(f'bhole{sx}', 0.0155, 0.01, 'chassis', (x, 0.0, MID), axis='X', seg=64); boolean_diff(wall, c); obs.append(wall)
        obs.append(annulus(f'gasket{sx}', 0.0158, 0.0185, 0.0008, 'foam', 0, n=96))
        g = obs[-1]; g.rotation_euler = (0, sx * math.pi / 2, 0); g.location = (x + sx * 0.0008, 0.0, MID)
    wall = rbox('baffle_back', 0.108, 0.0016, h, 0.002, 0.0004, 'chassis', (0.0, IN / 2 - 0.0016, FLOOR + 0.001), sp=4, se=1)
    c = cyl('prhole', 0.0145, 0.01, 'chassis', (0.031, IN / 2 - 0.0016, MID), axis='Y', seg=64); c.scale = (1.38, 1.0, 1.0)
    boolean_diff(wall, c)
    for nm, x, w2, hh in (('usbhole', 0.0, 0.0115, 0.0050), ('btnhole', BTN_X, 0.0110, 0.0110)):
        cc = box(nm, w2, 0.01, hh, x, IN / 2 - 0.0016, MID - hh / 2, 'chassis'); boolean_diff(wall, cc)
    obs.append(wall)
    for x in (-0.02, 0.02):                              # bosses for the board, with brass inserts
        for y in (-0.02, 0.02):
            obs.append(cyl(f'boss{x}{y}', 0.0028, PCB_Z - FLOOR, 'chassis', (x, y, FLOOR + (PCB_Z - FLOOR) / 2), seg=32))
            obs.append(cyl(f'insert{x}{y}', 0.0016, 0.003, 'brass', (x, y, PCB_Z - 0.0015 + 0.00002), seg=24))
    rib = bmesh.new()                                    # floor ribs tying baffles and bosses together
    add_box(rib, 0.0, -0.050, FLOOR, 0.106, 0.0016, 0.006); add_box(rib, 0.0, 0.020, FLOOR, 0.106, 0.0016, 0.004)
    add_box(rib, -0.020, 0.0, FLOOR, 0.0016, 0.10, 0.004); add_box(rib, 0.020, 0.0, FLOOR, 0.0016, 0.10, 0.004)
    obs.append(link('ribs', rib, 'chassis', smooth=False))
    for k, (x, y) in enumerate(((-0.034, 0.030), (0.034, 0.030), (-0.010, 0.040))):     # cable clips
        obs.append(box(f'clip{k}', 0.004, 0.003, 0.004, x, y, FLOOR, 'chassis', 0.0006))
    return obs

def driver(name, sx):
    """36 mm full-range driver (front towards ±x): basket flange, paper cone, rubber surround, dust cap, magnet, tabs."""
    part('spk', 'Drivers ×2, 36 mm full range, side-firing', 'neodymium, 4 Ω 3 W, Fs ≈ 380 Hz (e.g. PUI AS03604MR-N50-R class)',
         'mounted on the side baffles; stereo, widened by DSP')
    obs = [annulus(f'{name}_flange', 0.0152, 0.0180, 0.0007, 'speaker', 0.0),
           cone_shell(f'{name}_cone', 0.0062, 0.0142, 0.0032, 'cone', -0.0032),
           torus(f'{name}_surround', 0.0150, 0.0010, 'surround', 0.0, half=True),
           cyl(f'{name}_cap', 0.0058, 0.0011, 'speaker', (0, 0, -0.0002), seg=64),
           cyl(f'{name}_basket', 0.0150, 0.0016, 'speaker', (0, 0, -0.0040), seg=64),
           cyl(f'{name}_magnet', 0.0090, 0.0034, 'nickel', (0, 0, -0.0066), seg=64),
           box(f'{name}_tab1', 0.0018, 0.0010, 0.0035, 0.0125, 0.0040, -0.0060, 'term'),
           box(f'{name}_tab2', 0.0018, 0.0010, 0.0035, 0.0125, -0.0040, -0.0060, 'term')]
    g = group(name, obs)
    g.rotation_euler = (0, sx * math.pi / 2, 0)          # +z (the front) turned to ±x
    g.location = (sx * (IN / 2 - 0.0016 - 0.0012), 0.0, MID)
    return g

def radiator():
    part('pr', 'Passive radiator 48 × 34 mm, behind the back grille', 'oval, aluminium plate on a rubber surround (e.g. Tymphany PR class)',
         'tuned to the ≈ 300 cm³ sealed interior: the bass the small drivers cannot make')
    obs = []
    # 48 × 34 mm: the widest oval that fits right of the USB-C on the back (the 60 mm first asked for does not)
    fr = cyl('pr_frame', 0.0170, 0.0012, 'speaker', (0, 0, 0.0006), seg=96); fr.scale = (1.41, 1.0, 1.0)
    sur = cyl('pr_surround', 0.0152, 0.0016, 'surround', (0, 0, 0.0018), seg=96); sur.scale = (1.41, 1.0, 1.0)
    pl = cyl('pr_plate', 0.0122, 0.0008, 'nickel', (0, 0, 0.0028), seg=96); pl.scale = (1.41, 1.0, 1.0)
    obs += [fr, sur, pl]
    for k, (x, y) in enumerate(((-0.0215, 0.0), (0.0215, 0.0), (0.0, 0.0150), (0.0, -0.0150))):
        obs.append(cyl(f'pr_screw{k}', 0.0011, 0.0006, 'screw', (x, y, 0.0015), seg=16))
    g = group('radiator', obs)
    g.rotation_euler = (-math.pi / 2, 0, 0)                # +z (the front) turned to +y, towards the back grille
    g.location = (0.031, IN / 2 - 0.0016 - 0.0040, MID)   # frame on the baffle, plate in its opening
    return g

def battery():
    part('batt', 'Backup cell, Li-ion pouch 1000 mAh 3.7 V', '503450 cell, protection board (DW01A + FS8205), nickel tabs, JST PH lead',
         '3.7 Wh: ≈ 9 h of standby plus the alarm sound if the power goes; never runs the room')
    z = FLOOR + 0.0012; obs = []                       # on a foam pad over the light-ring board
    obs.append(box('foam_pad', 0.032, 0.046, 0.0008, 0.0, 0.010, z - 0.0004, 'foam'))
    obs.append(box('cell', 0.0316, 0.047, 0.005, 0.0, 0.0095, z + 0.0004, 'battery', 0.0015))   # 34 mm wide with its folds
    obs.append(box('cell_seal', 0.034, 0.003, 0.0006, 0.0, 0.0345, z + 0.0026, 'battery'))
    for sx in (-1, 1):                                  # folded side seals
        obs.append(box(f'cell_fold{sx}', 0.0012, 0.044, 0.0045, sx * 0.0164, 0.0095, z + 0.0006, 'battery', 0.0004))
    obs.append(box('pcm', 0.030, 0.004, 0.0008, 0.0, 0.0385, z + 0.0026, 'pcb'))
    obs.append(box('pcm_ic', 0.003, 0.0016, 0.0009, -0.005, 0.0385, z + 0.0034, 'chip'))
    obs.append(box('pcm_fet', 0.003, 0.0016, 0.0009, 0.004, 0.0385, z + 0.0034, 'chip'))
    for sx in (-1, 1):
        obs.append(box(f'tab{sx}', 0.003, 0.004, 0.0001, sx * 0.009, 0.0355, z + 0.0034, 'nickel'))
    obs.append(box('batt_label', 0.026, 0.034, 0.00002, 0.0, 0.007, z + 0.0054, 'label'))
    if not LINE:
        obs.append(label('Li-ion  3.7 V  1000 mAh  3.7 Wh', 0.0019, (0.0, 0.010, z + 0.00545), (0, 0, math.pi / 2), 'chip'))
        obs.append(label('503450  UN38.3  IEC 62133', 0.0012, (0.006, 0.010, z + 0.00545), (0, 0, math.pi / 2), 'chip'))
    return obs

def bottom():
    part('plate', 'Bottom plate', 'PC/ABS, 2.0 mm, four M2.5 × 6 Phillips screws into the chassis', 'screws hidden under the rubber disc')
    part('ring', 'Light ring underneath: 24 RGB LEDs + light guide', 'Worldsemi WS2812B-2020 on a ring board, PMMA guide Ø69 mm',
         'shines out through the 2.2 mm gap onto the nightstand; JST SH lead to the main board')
    part('disc', 'Rubber foot disc Ø68 mm', 'TPE, 2.2 mm, adhesive', 'covers the screws')
    obs = [rbox('plate', IN - 0.0004, IN - 0.0004, WALL, 0.003, 0.0004, 'chassis', (0, 0, PL), sp=4, se=1)]
    rib = bmesh.new()
    for x in (-0.045, 0.045): add_box(rib, x, 0.0, FLOOR, 0.0012, 0.09, 0.0018)
    for y in (-0.045, 0.045): add_box(rib, 0.0, y, FLOOR, 0.09, 0.0012, 0.0018)
    obs.append(link('plate_ribs', rib, 'chassis', smooth=False))
    for x in (-0.02, 0.02):
        for y in (-0.02, 0.02):
            obs.append(annulus(f'cbore{x}{y}', 0.0014, 0.0030, 0.0008, 'chassis', FLOOR, loc=(x, y)))
    obs.append(annulus('ring_pcb', 0.0315, 0.0375, 0.0008, 'pcb', FLOOR))
    lb, ld = bmesh.new(), bmesh.new()
    for k in range(24):
        a = 2 * math.pi * k / 24; x, y = 0.0345 * math.cos(a), 0.0345 * math.sin(a)
        add_box(lb, x, y, FLOOR + 0.0008, 0.002, 0.002, 0.0009)
        add_box(ld, x, y, FLOOR + 0.0017, 0.0007, 0.0007, 0.00003)
    obs.append(link('ring_leds', lb, 'led', smooth=False)); obs.append(link('ring_dies', ld, 'chip', smooth=False))
    obs.append(box('ring_jst', 0.0058, 0.0035, 0.0029, -0.0345, 0.0, FLOOR + 0.0008, 'jst'))
    obs.append(annulus('guide', 0.0335, 0.0351, 0.0040, 'pmma', 0.0002))
    obs.append(cyl('disc', 0.034, PL, 'rubber', (0, 0, PL / 2), seg=128))
    return obs

def screws_bottom():
    obs = []
    for x in (-0.02, 0.02):
        for y in (-0.02, 0.02): obs += screw(f'bscrew{x}{y}', x, y, PL - 0.0001, 0.00125, 0.006, up=False)
    return obs

def screws_board():
    obs = []
    for x in (-0.02, 0.02):
        for y in (-0.02, 0.02): obs += screw(f'pscrew{x}{y}', x, y, ZT + 0.0001, 0.0010, 0.004)
    return obs

def shift(obs, dx=0.0, dy=0.0, dz=0.0):
    for o in obs: o.location = (o.location.x + dx, o.location.y + dy, o.location.z + dz)
    return obs

EXPLODE = {   # group → (dx, dy, dz) in the exploded drawing
    'bottom_disc': (0, 0, -0.140), 'bottom_screws': (0, 0, -0.105), 'bottom_ring': (0, 0, -0.060), 'bottom_plate': (0, 0, 0),
    'battery': (0, -0.080, 0.030), 'chassis': (0, 0, 0.090), 'drivers': (0.075, 0, 0.090), 'radiator': (0, 0.030, 0.090),
    'board': (0, 0, 0.140), 'board_screws': (0, 0, 0.170), 'display': (0, -0.100, 0.135), 'top': (0, 0, 0.215), 'shell': (0, 0, 0.300),
}

def build_exploded():
    bot = bottom()
    groups = {'bottom_disc': [o for o in bot if o.name == 'disc'], 'bottom_screws': screws_bottom(),
              'bottom_ring': [o for o in bot if o.name.startswith(('ring_', 'guide'))],
              'bottom_plate': [o for o in bot if o.name.startswith(('plate', 'cbore'))],
              'battery': battery(), 'chassis': chassis(), 'drivers': [driver('drv_l', -1), driver('drv_r', 1)],
              'radiator': [radiator()], 'board': main_board(), 'board_screws': screws_board(),
              'display': display(), 'top': top_inside(), 'shell': shell()}
    for k, obs in groups.items():
        dx, dy, dz = EXPLODE[k]
        if k == 'drivers':                                        # each driver slides out of its own side
            for o in obs: o.location.x += dx * (1 if o.location.x > 0 else -1); o.location.z += dz
        else: shift(obs, dx, dy, dz)
    off = lambda k, p: (p[0] + EXPLODE[k][0], p[1] + EXPLODE[k][1], p[2] + EXPLODE[k][2])
    def sag(a, b, drop=0.012, out=(0, 0)):                         # a cable from a to b, hanging a little
        m = ((a[0] + b[0]) / 2 + out[0], (a[1] + b[1]) / 2 + out[1], min(a[2], b[2]) - drop)
        return [a, ((a[0] + m[0]) / 2, (a[1] + m[1]) / 2, a[2] - drop * 0.4), m, ((b[0] + m[0]) / 2, (b[1] + m[1]) / 2, b[2] - drop * 0.4), b]
    cab = []
    for sx, j in ((-1, 'j_spk_l'), (1, 'j_spk_r')):                 # driver tabs → board
        a = (sx * (IN / 2 - 0.0016 - 0.0012 - 0.0060) + sx * EXPLODE['drivers'][0], 0.0, MID - 0.0125 + EXPLODE['drivers'][2])
        b = off('board', (sx * 0.028, 0.008, ZT + 0.0030))
        cab += wires(f'spk{sx}_w', sag(a, b, 0.010), ['wire_r', 'wire_k'])
    cab += wires('batt_w', sag(off('battery', (0.0, 0.0385, FLOOR + 0.0045)), off('board', (0.022, 0.0395, ZT + 0.006)), 0.004, (0.02, 0.0)), ['wire_r', 'wire_k'], gap=0.0016, r=0.0006)
    cab += wires('ring_w', sag(off('bottom_ring', (-0.0345, 0.0, FLOOR + 0.0035)), off('board', (-0.026, 0.034, ZT + 0.003)), 0.004, (-0.03, 0.0)), ['wire_w', 'wire_r', 'wire_k'])
    cab += wires('pins_w', sag(off('top', (0.0085, PIN_Y, CEIL - 0.0080)), off('board', (0.0, -0.030, ZT + 0.003)), 0.004, (0.02, 0.0)), ['wire_w', 'wire_r', 'wire_k'])
    cab.append(tail_flex('touch_flex', 0.026, -0.0275, off('top', (0, 0, CEIL - 0.0002))[2], off('board', (0, 0, ZT + 0.0025))[2]))
    d0 = off('display', (-0.002, -IN / 2 + 0.006, MID - 0.014)); d1 = off('board', (-0.002, -0.0425, ZT + 0.0012))
    cab.append(flex('disp_flex', [d0, (d0[0], d0[1] + 0.01, d0[2] - 0.012), (d1[0], d1[1] - 0.02, d1[2] - 0.006), d1], 0.010))
    groups['cables'] = cab
    g = group('explode', [o for obs in groups.values() for o in obs])
    bpy.context.view_layer.update()
    def at(name, fx=0.5, fy=0.5, fz=1.0):          # a point on an object's world bounding box (fz 1 = its top)
        o = bpy.data.objects[name]; cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        lo = [min(c[i] for c in cs) for i in range(3)]; hi = [max(c[i] for c in cs) for i in range(3)]
        return tuple(lo[i] + (hi[i] - lo[i]) * f for i, f in enumerate((fx, fy, fz)))
    EXPLODE_PTS.update({
        'shell': at('shell', 0.5, 0.5, 1.0), 'pins': at('pin_tip0'), 'magnets': at('magnet1'), 'touch': at('electrode', 0.8, 0.85),
        'matrix': at('diffuser', 0.3, 0.0, 0.5), 'status': at('lightpipe', 0.5, 0.0, 0.5), 's3': at('s3_can'), 'h2': at('h2_can'),
        'usbc': at('usbc_rx'), 'btn': at('btn_cap'), 'spk': at('drv_r_cap', 1.0, 0.5, 0.5), 'pr': at('pr_plate', 0.5, 1.0, 0.5),
        'chassis': at('baffle_side1', 0.5, 0.3), 'batt': at('cell', 0.5, 0.3), 'plate': at('plate', 0.8, 0.2),
        'ring': at('guide', 0.85, 0.5), 'disc': at('disc', 0.5, 0.2)})
    return g

EXPLODE_PTS = {}

# ---------------------------------------------------------------------------------------------------------------
# Photoreal exploded view (owner, 2026-10-30: "come apparirebbe smontata nei minimi dettagli"): real materials, a
# routed board texture, product-shot light.
def pcb_traces(name='traces', px_mm=24):
    """Copper traces and vias under the solder mask: Manhattan routes between part pads, as a factor image."""
    import numpy as np
    w_mm, d_mm = 64, 88; Wp, Hp = w_mm * px_mm, d_mm * px_mm; a = np.zeros((Hp, Wp), dtype=np.float32)
    rng = random.Random(3)
    def px(x, y): return int((x / 0.064 + 0.5) * (Wp - 1)), int(((y + 0.002) / 0.088 + 0.5) * (Hp - 1))
    pads = [(rng.uniform(-0.03, 0.03), rng.uniform(-0.04, 0.04)) for _ in range(260)]
    for k in range(420):
        (x0, y0), (x1, y1) = rng.choice(pads), rng.choice(pads)
        (i0, j0), (i1, j1) = px(x0, y0), px(x1, y1); t = rng.choice((2, 3, 3, 5))
        jm = j0 if rng.random() < 0.5 else j1
        a[max(0, jm - t // 2):jm + t // 2 + 1, min(i0, i1):max(i0, i1) + 1] = 1.0
        a[min(j0, j1):max(j0, j1) + 1, max(0, (i1 if jm == j0 else i0) - t // 2):(i1 if jm == j0 else i0) + t // 2 + 1] = 1.0
    for _ in range(700):
        i, j = rng.randrange(4, Wp - 4), rng.randrange(4, Hp - 4); a[j - 3:j + 4, i - 3:i + 4] = 0.6
    # keep the antenna areas clean
    for x0, x1 in ((-0.029, -0.011), (0.0114, 0.0246)):
        (i0, j0), (i1, j1) = px(x0, -0.046), px(x1, -0.039); a[j0:j1, i0:i1] = 0.0
    img = bpy.data.images.new(name, Wp, Hp, alpha=False)
    rgba = np.ones((Hp, Wp, 4), dtype=np.float32); rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = a
    img.pixels.foreach_set(rgba.ravel()); img.pack(); return img

def real_mats():
    def p(name, hexc, **kw): MATS[name] = principled(name, srgb(hexc), **kw)
    p('pcb', '#111316', rough=0.32, coat=0.6)                     # black solder mask, glossy
    p('chip', '#18191b', rough=0.45)                              # epoxy mould
    p('shield', '#cdd0d4', metal=1.0, rough=0.2)                  # tin-plated cans, USB-C shell
    p('speaker', '#1a1b1d', rough=0.55)
    p('cone', '#2d2e31', rough=0.92)                              # treated paper
    p('surround', '#121214', rough=0.7)
    p('battery', '#c9cbce', metal=0.85, rough=0.32)               # aluminium-laminate pouch
    p('copper', '#c07a3a', metal=1.0, rough=0.28)
    p('chassis', '#3a3c41', rough=0.5)                            # glass-filled PC
    p('magnet', '#d8dadd', metal=1.0, rough=0.15)
    p('nickel', '#c3c5c8', metal=1.0, rough=0.25)
    p('screw', '#1f2023', metal=1.0, rough=0.3)                   # black zinc
    p('led', '#f2efe6', rough=0.35)
    p('alcap', '#e8c95a', rough=0.4)                              # LED phosphor dots, electrolytic top
    p('kapton', '#c97c25', rough=0.3, coat=0.5)
    p('etch', '#9a9da2', metal=1.0, rough=0.55)
    p('label', '#efefec', rough=0.7)
    p('silk', '#ececea', rough=0.6)
    p('mlcc', '#b89a6c', rough=0.5)
    p('res', '#141516', rough=0.4)
    p('term', '#d4d6d9', metal=1.0, rough=0.25)
    p('jst', '#f1efe9', rough=0.45)
    p('foam', '#4a4b4f', rough=0.95)
    p('brass', '#c9a25a', metal=1.0, rough=0.3)
    p('wire_r', '#b5221c', rough=0.4); p('wire_k', '#141414', rough=0.4); p('wire_w', '#e9e9e6', rough=0.4)
    g = principled('pmma', srgb('#ffffff'), rough=0.04); b = g.node_tree.nodes['Principled BSDF']
    b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.49; MATS['pmma'] = g
    # main board: solder mask with the copper routing showing through as slightly raised, lighter lines
    m = principled('pcb_main', srgb('#111316'), rough=0.3, coat=0.6); nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = pcb_traces(); tx.interpolation = 'Linear'
    nt.links.new(tc.outputs['Generated'], tx.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[6].default_value = srgb('#111316'); mix.inputs[7].default_value = srgb('#1f2a2c')
    nt.links.new(tx.outputs['Color'], mix.inputs['Factor']); nt.links.new(mix.outputs[2], bs.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.00003
    nt.links.new(tx.outputs['Color'], bp.inputs['Height']); nt.links.new(bp.outputs[0], bs.inputs['Normal'])
    MATS['pcb_main'] = m

def real_explode():
    real_mats()
    scene.render.film_transparent = True                 # laid on the page colour afterwards: no box round it
    build_exploded()
    world(srgb('#d9dadc'), 0.45)
    area('softbox', (0.1, -0.25, 1.0), (0, 0, 0.1), 1.6, 42)          # big top light: soft, clean reflections
    area('key', (-0.7, -0.6, 0.6), (0, 0, 0.1), 0.7, 30)
    area('rim', (0.4, 0.8, 0.5), (0, 0, 0.12), 0.6, 30)
    area('kick', (0.8, -0.3, 0.1), (0, 0, 0.08), 0.5, 8)
    look((0.52, -0.52, 0.66), (0.0, -0.01, 0.105), 60)
    try: scene.view_settings.look = 'AgX - Medium High Contrast'
    except TypeError: pass
    scene.view_settings.exposure = 0.0
    bpy.context.view_layer.update()
    cam = scene.camera; rx, ry = scene.render.resolution_x, scene.render.resolution_y
    pts = {k: [round(v.x * rx, 1), round((1 - v.y) * ry, 1)] for k, v in
           ((k, world_to_camera_view(scene, cam, Vector(p))) for k, p in EXPLODE_PTS.items())}
    with open(os.path.join(OUT, 'explode-real.json'), 'w') as f: json.dump({'size': [rx, ry], 'points': pts}, f, indent=1)
