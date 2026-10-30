# AuraWake base, inside (owner, 2026-10-30: "come se dovessi farla funzionare"). Every part is a catalogue part at its
# datasheet size, placed where it sits in the 120 × 120 × 45 mm enclosure; build_exploded() pulls them apart along Z
# (and the side speakers along X, the display board along −Y) for the exploded drawing. Loaded by aura.py with exec(),
# so it shares its helpers (rbox, cyl, link, group, M, W, H, PL, TOP, MID, BTN_X …). Metres throughout.
WALL = 0.002                       # shell wall and top thickness (PC/ABS, satin)
IN = W - 2 * WALL                  # 116 mm inside
FLOOR = PL + WALL                  # top of the bottom plate, 4.2 mm
CEIL = TOP - WALL                  # underside of the top, 43.0 mm
PCB_Z = MID - 0.0016 - 0.0012      # main board: its top 1.6 mm under the USB-C centre line (mid-mount receptacle)
BOM = []                           # (key, part, maker / code, notes) for the parts list

def part(key, text, code, note=''):
    if not any(b[0] == key for b in BOM): BOM.append((key, text, code, note))

def box(name, w, d, h, x, y, z, mat, r=0.0):
    """A component as a box: w (x) × d (y) × h (z), its base centre at (x, y, z)."""
    return rbox(name, w, d, h, r, min(r, h / 3) if r else 0.0, mat, (x, y, z), sp=4 if r else 1, se=1)

def shell():
    part('shell', 'Enclosure: top and four walls in one piece', 'PC/ABS, satin, 2.0 mm walls',
         'side and back speaker grilles, front micro-perforation for the time, USB-C and button openings')
    outer = rbox('shell', W, W, H, EDGE_P, EDGE_T, 'body', (0, 0, PL), sp=4, se=2)
    cutter = rbox('shell_in', IN, IN, H - WALL + 0.001, 0.001, 0.0, 'body', (0, 0, PL - 0.001), sp=2)
    boolean_diff(outer, cutter)
    return [outer]

def top_inside():
    """Under the top: the touch electrode, the pin block and the two centring magnets."""
    part('touch', 'Touch electrode under the top (palm)', 'copper on 0.1 mm polyimide, 100 × 76 mm',
         'read by the ESP32-S3 capacitive touch; a 3 mm keep-out round the pins and magnets')
    part('pins', 'Bracelet charging contacts, 3 positions, 4 mm pitch', 'Mill-Max 0906 series spring pins on a carrier, gold',
         'sealed with a silicone gasket; powered only when the bracelet ID answers')
    part('magnets', 'Centring magnets ×2', 'N52 NdFeB disc Ø6 × 2 mm', 'pull the bracelet’s flat edge onto the pins, one way only')
    y = -W / 2 + 0.020; obs = []
    obs.append(box('electrode', 0.100, 0.076, 0.0001, 0, 0.012, CEIL - 0.0001, 'copper'))
    obs.append(box('pin_board', 0.022, 0.008, 0.0010, 0, y, CEIL - 0.0042, 'pcb'))
    obs.append(box('gasket', 0.016, 0.005, 0.0015, 0, y, CEIL - 0.0015, 'rubber', 0.001))
    for i in (-1, 0, 1):
        obs.append(cyl(f'pin_barrel{i}', 0.0009, 0.0030, 'gold', (i * 0.004, y, CEIL - 0.0032 + 0.0015), seg=24))
        obs.append(cyl(f'pin_tip{i}', 0.00075, 0.0024, 'gold', (i * 0.004, y, CEIL + 0.0004), seg=24))
    for sx in (-1, 1):
        obs.append(cyl(f'magnet{sx}', 0.003, 0.002, 'magnet', (sx * 0.013, y, CEIL - 0.001), seg=32))
        obs.append(box(f'magnet_cup{sx}', 0.008, 0.008, 0.0004, sx * 0.013, y, CEIL - 0.0024, 'chassis'))
    return obs

def display():
    """Behind the front wall: the dot matrix for the time, its baffle and diffuser, the front LED, light sensor, mic."""
    part('matrix', 'Time display: 0402 warm-white LEDs on a 1.33 mm grid', '351 positions, driver Lumissil IS31FL3741 (I²C)',
         'black baffle grid + diffuser film behind ~0.1 mm laser micro-holes in a 0.5 mm thinned window of the front wall')
    part('status', 'Front status LED (day): RGB with a light pipe', 'Everlight 99-235 RGB + PC light pipe Ø1.7 mm', '')
    part('als', 'Ambient light sensor', 'Vishay VEML7700 (I²C)', 'picks the light channel and brightness')
    part('mic', 'Microphone (snoring, noise; never recorded)', 'Knowles SPH0645LM4H, I²S MEMS', 'port through the front micro-holes')
    y = -IN / 2 + 0.0012; obs = []
    obs.append(box('disp_pcb', 0.066, 0.0012, 0.026, -0.002, y + 0.0040, MID - 0.013, 'pcb'))
    obs.append(box('baffle', 0.050, 0.0030, 0.013, -0.006, y + 0.0010, MID - 0.0065, 'chassis'))
    obs.append(box('diffuser', 0.050, 0.0003, 0.013, -0.006, y - 0.0005, MID - 0.0065, 'pmma'))
    pitch = PU / 3
    for c in range(25):
        for r in range(7):
            obs.append(box(f'led{c}_{r}', 0.0010, 0.0005, 0.0005, -0.006 + (c - 12) * pitch, y + 0.0025, MID - 0.00025 + (3 - r) * pitch, 'led'))
    obs.append(box('drv', 0.006, 0.0008, 0.006, 0.020, y + 0.0049, MID - 0.003, 'chip'))
    obs.append(cyl('lightpipe', 0.00085, 0.0042, 'pmma', (0.036, y + 0.0013, MID), axis='Y', seg=24))
    obs.append(box('rgb', 0.0016, 0.0008, 0.0016, 0.036, y + 0.0036, MID - 0.0008, 'chip'))
    obs.append(box('als_chip', 0.0068, 0.0008, 0.0035, 0.028, y + 0.0040, MID + 0.005, 'chip'))
    obs.append(box('mic_chip', 0.0035, 0.0010, 0.0026, 0.028, y + 0.0040, MID - 0.009, 'shield'))
    obs.append(box('fpc_disp', 0.010, 0.012, 0.0002, -0.002, y + 0.012, MID - 0.0132, 'copper'))
    return obs

def main_board():
    part('pcb', 'Main board, 4 layers, 1.0 mm', 'FR-4, 64 × 100 mm', 'between the speaker chambers; USB-C and button on its back edge')
    part('s3', 'Wi-Fi + BLE: the brain', 'Espressif ESP32-S3-WROOM-1-N16R8', 'routines, ramps, Matter controller, app link')
    part('h2', 'Thread / Matter radio (border router)', 'Espressif ESP32-H2-MINI-1', 'talks to lamp, shutters, diffuser')
    part('amp', 'Audio amplifiers ×2, 3.2 W class D', 'Analog Devices MAX98357A (I²S)', '')
    part('pd', 'USB-C power: asks the charger for 5 V 3 A', 'ST STUSB4500 PD sink', '15 W in')
    part('chg', 'Backup battery charger + power path', 'TI BQ24074', 'runs everything from USB, tops up the cell')
    part('buck', '3.3 V regulator', 'TI TPS62133 buck, 3 A', '')
    part('gauge', 'Battery fuel gauge', 'Analog Devices MAX17048', '')
    part('rtc', 'Real-time clock on the battery', 'NXP PCF85063A + 32.768 kHz crystal', 'keeps 06:30 through a power cut')
    part('lsw', 'Bracelet pin power switch, current-limited', 'TI TPS2553 (300 mA limit)', 'on only after the ID line answers')
    part('usbc', 'USB-C receptacle, mid-mount, 16 pins', 'GCT USB4105', '')
    part('btn', 'Pairing button (tactile switch + cap)', 'C&K PTS526, 6 × 4 mm', 'behind the round cap at the back')
    z = PCB_Z; t = 0.0010; zt = z + t; obs = []
    obs.append(box('main_pcb', 0.064, 0.100, t, 0, 0.004, z, 'pcb'))
    obs.append(box('s3_mod', 0.018, 0.0255, 0.0024, -0.012, -0.012, zt, 'pcb'))
    obs.append(box('s3_can', 0.015, 0.018, 0.0008, -0.012, -0.0155, zt + 0.0024, 'shield'))
    obs.append(box('h2_mod', 0.0132, 0.0166, 0.0016, 0.016, -0.016, zt, 'pcb'))
    obs.append(box('h2_can', 0.0110, 0.0110, 0.0008, 0.016, -0.0185, zt + 0.0016, 'shield'))
    for i, x in enumerate((-0.020, 0.020)):
        obs.append(box(f'amp{i}', 0.003, 0.003, 0.0008, x, 0.020, zt, 'chip'))
    obs.append(box('pd_ic', 0.004, 0.004, 0.0008, 0.008, 0.040, zt, 'chip'))
    obs.append(box('chg_ic', 0.003, 0.004, 0.0008, 0.016, 0.030, zt, 'chip'))
    obs.append(box('buck_ic', 0.003, 0.003, 0.0008, -0.004, 0.030, zt, 'chip'))
    obs.append(box('inductor', 0.004, 0.004, 0.0020, -0.010, 0.030, zt, 'chip', 0.0006))
    obs.append(box('gauge_ic', 0.002, 0.002, 0.0006, 0.022, 0.024, zt, 'chip'))
    obs.append(box('rtc_ic', 0.003, 0.003, 0.0008, -0.022, 0.004, zt, 'chip'))
    obs.append(box('xtal', 0.0032, 0.0015, 0.0008, -0.022, 0.000, zt, 'shield'))
    obs.append(box('lsw_ic', 0.003, 0.003, 0.0008, 0.000, -0.034, zt, 'chip'))
    for i in range(10):                                   # passives along the rails
        obs.append(box(f'cap{i}', 0.0016, 0.0008, 0.0008, -0.026 + i * 0.0056, 0.012, zt, 'chip'))
    obs.append(box('usbc_rx', 0.0089, 0.0073, 0.0032, 0, W / 2 - WALL - 0.0036, z - 0.0011, 'shield', 0.0012))
    obs.append(box('btn_sw', 0.006, 0.0035, 0.004, BTN_X, W / 2 - WALL - 0.0018, MID - 0.002, 'chip'))
    for name, x, y in (('j_disp', -0.002, -0.044), ('j_batt', 0.010, 0.050), ('j_spk_l', -0.028, 0.040), ('j_spk_r', 0.028, 0.040),
                       ('j_ring', -0.010, 0.050), ('j_pins', 0.0, -0.040)):
        obs.append(box(name, 0.006, 0.0035, 0.0018, x, y, zt, 'chassis'))
    return obs

def chassis():
    part('chassis', 'Inner chassis: two sealed speaker chambers + board bosses', 'PC-GF10, one moulding',
         'chambers 22 × 56 × 34 mm (≈ 40 cm³ each), ported to the back grille; four M2.5 bosses to the bottom plate')
    part('spk', 'Speakers ×2, full range, side-firing', '28 × 40 mm rectangular, 4 Ω 3 W (e.g. PUI AS04004PO-2-R class)',
         'through the side grilles; mesh behind the holes')
    obs = []
    for sx in (-1, 1):
        x = sx * (IN / 2 - 0.011 - 0.0035)
        obs.append(box(f'chamber{sx}', 0.022, 0.056, 0.034, x, 0.0, FLOOR, 'chassis', 0.002))
        obs.append(box(f'port{sx}', 0.008, 0.010, 0.006, x, 0.033, FLOOR + 0.004, 'chassis', 0.001))
    for x in (-0.02, 0.02):
        for y in (-0.02, 0.02):
            obs.append(cyl(f'boss{x}{y}', 0.0028, PCB_Z - FLOOR, 'chassis', (x, y, FLOOR + (PCB_Z - FLOOR) / 2), seg=24))
    obs.append(box('bar_front', 0.064, 0.004, 0.006, 0, -0.050, FLOOR, 'chassis'))
    obs.append(box('bar_back', 0.064, 0.004, 0.006, 0, 0.054, FLOOR, 'chassis'))
    return obs

def speakers():
    obs = []
    for sx in (-1, 1):
        x = sx * (IN / 2 - 0.0035)
        fr = rbox(f'spk_frame{sx}', 0.007, 0.040, 0.028, 0.002, 0.0006, 'speaker', (x, 0.0, MID - 0.014), sp=4, se=1)
        cone = rbox(f'spk_cone{sx}', 0.0012, 0.032, 0.020, 0.004, 0.0003, 'cone', (x + sx * 0.0035, 0.0, MID - 0.010), sp=6, se=1)
        dome = cyl(f'spk_dome{sx}', 0.0045, 0.0012, 'speaker', (x + sx * 0.0042, 0.0, MID), axis='X', seg=32)
        mag = cyl(f'spk_mag{sx}', 0.007, 0.004, 'magnet', (x - sx * 0.0045, 0.0, MID), axis='X', seg=32)
        obs += [fr, cone, dome, mag]
    return obs

def battery():
    part('batt', 'Backup cell, Li-ion pouch 1000 mAh 3.7 V', '503450 cell with protection board',
         '3.7 Wh: ≈ 10 h of standby plus the alarm sound if the power goes; never runs the room')
    z = FLOOR + 0.0012; obs = []                     # on top of the light-ring board (0.8 mm) with a foam pad
    obs.append(box('cell', 0.034, 0.050, 0.005, 0.0, 0.012, z, 'battery', 0.001))
    obs.append(box('pcm', 0.030, 0.004, 0.0035, 0.0, 0.0385, z, 'pcb'))
    obs.append(curve('batt_lead', [(0.004, 0.040, z + 0.003), (0.008, 0.047, z + 0.008), (0.010, 0.050, PCB_Z)], 0.0006, 'cable'))
    return obs

def bottom():
    part('plate', 'Bottom plate', 'PC/ABS, 2.0 mm, four M2.5 × 6 screws into the chassis', 'screws hidden under the rubber disc')
    part('ring', 'Light ring underneath: 24 RGB LEDs + light guide', 'Worldsemi WS2812B-2020 on a ring board, PMMA guide Ø69 mm',
         'shines out through the 2.2 mm gap onto the nightstand')
    part('disc', 'Rubber foot disc Ø68 mm', 'TPE, 2.2 mm', 'covers the screws')
    obs = [box('plate', IN - 0.0004, IN - 0.0004, WALL, 0, 0, PL, 'chassis')]
    obs.append(annulus('ring_pcb', 0.0315, 0.0375, 0.0008, 'pcb', FLOOR))
    for k in range(24):
        a = 2 * math.pi * k / 24
        obs.append(box(f'rgb{k}', 0.002, 0.002, 0.0009, 0.0345 * math.cos(a), 0.0345 * math.sin(a), FLOOR + 0.0008, 'led'))
    obs.append(annulus('guide', 0.0335, 0.0351, 0.0040, 'pmma', 0.0002))
    obs.append(cyl('disc', 0.034, PL, 'rubber', (0, 0, PL / 2), seg=128))
    for x in (-0.02, 0.02):
        for y in (-0.02, 0.02):
            obs.append(cyl(f'screw{x}{y}', 0.00125, 0.006, 'screw', (x, y, PL + 0.002), seg=16))
            obs.append(cyl(f'screwhead{x}{y}', 0.0022, 0.0012, 'screw', (x, y, PL - 0.0006), seg=24))
    return obs

def annulus(name, r_in, r_out, h, mat, z, n=96):
    """A flat ring (board or light guide), its base at z."""
    bm = bmesh.new(); vs = []
    for i in range(n):
        a = 2 * math.pi * i / n; c, sn = math.cos(a), math.sin(a)
        vs.append([bm.verts.new((r * c, r * sn, zz)) for r, zz in ((r_in, 0), (r_out, 0), (r_out, h), (r_in, h))])
    for i in range(n):
        A, B = vs[i], vs[(i + 1) % n]
        for k in range(4): bm.faces.new((A[k], B[k], B[(k + 1) % 4], A[(k + 1) % 4]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return link(name, bm, mat, (0, 0, z))

def shift(obs, dx=0.0, dy=0.0, dz=0.0):
    for o in obs: o.location = (o.location.x + dx, o.location.y + dy, o.location.z + dz)
    return obs

EXPLODE = {   # group → (dx, dy, dz) in the exploded drawing
    'bottom_disc': (0, 0, -0.130), 'bottom_screws': (0, 0, -0.095), 'bottom_ring': (0, 0, -0.055), 'bottom_plate': (0, 0, 0),
    'battery': (0, 0, 0.035), 'chassis': (0, 0, 0.095), 'speakers': (0.080, 0, 0.095), 'board': (0, 0, 0.140),
    'display': (0, -0.100, 0.135), 'top': (0, 0, 0.210), 'shell': (0, 0, 0.300),
}

def build_exploded():
    bot = bottom()
    disc = [o for o in bot if o.name == 'disc']
    screws = [o for o in bot if o.name.startswith('screw')]
    ring = [o for o in bot if o.name.startswith(('ring_pcb', 'rgb', 'guide'))]
    plate = [o for o in bot if o.name == 'plate']
    groups = {'bottom_disc': disc, 'bottom_screws': screws, 'bottom_ring': ring, 'bottom_plate': plate,
              'battery': battery(), 'chassis': chassis(), 'speakers': speakers(), 'board': main_board(),
              'display': display(), 'top': top_inside(), 'shell': shell()}
    for k, obs in groups.items():
        dx, dy, dz = EXPLODE[k]
        if k == 'speakers':                                       # each speaker slides out of its own side
            for o in obs: o.location.x += dx * (1 if o.location.x > 0 else -1); o.location.z += dz
        else: shift(obs, dx, dy, dz)
    g = group('explode', [o for obs in groups.values() for o in obs])
    bpy.context.view_layer.update()
    def at(name, fx=0.5, fy=0.5, fz=1.0):          # a point on an object's world bounding box (fz 1 = its top)
        o = bpy.data.objects[name]; cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        lo = [min(c[i] for c in cs) for i in range(3)]; hi = [max(c[i] for c in cs) for i in range(3)]
        return tuple(lo[i] + (hi[i] - lo[i]) * f for i, f in enumerate((fx, fy, fz)))
    EXPLODE_PTS.update({
        'shell': at('shell', 0.5, 0.5, 1.0), 'pins': at('pin_tip0'), 'magnets': at('magnet1'), 'touch': at('electrode', 0.75, 0.8),
        'matrix': at('diffuser', 0.3, 0.0, 0.5), 'status': at('lightpipe', 0.5, 0.0, 0.5), 's3': at('s3_can'), 'h2': at('h2_can'),
        'usbc': at('usbc_rx'), 'btn': at('btn_sw'), 'spk': at('spk_cone1', 1.0, 0.5, 0.5), 'chassis': at('chamber1', 0.5, 0.2),
        'batt': at('cell', 0.5, 0.3), 'plate': at('plate', 0.8, 0.2), 'ring': at('guide', 0.85, 0.5), 'disc': at('disc', 0.5, 0.2)})
    return g

EXPLODE_PTS = {}
