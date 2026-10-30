# AuraWake · one night in a bedroom (owner, 2026-10-30: "scene pulite, premium, minimal, stile Apple, vibe lifestyle").
# One fixed camera at nightstand height; only the light changes. Frames (spec §6):
#   1 22:00 take the bracelet: lamp 2200 K 40 %, violet ring, shutters closing, dusk outside
#   2 22:40 asleep: everything off, shutters closed
#   3 03:12 awake for a moment: the time on, dim and warm
#   4 06:14 the wake-up: dawn lamp, shutters opening, amber ring
#   5 06:16 a palm on the base: lamp towards 5000 K, more daylight
# Loaded by aura.py (exec) in real mode: shots room1 … room5. Base at the origin, the nightstand top at z = 0.
FRAME = int(SHOT[4]) if SHOT.startswith('room') and SHOT[4:].isdigit() else 0
ROOM = {   # time, lamp (power W, colour), ring colour or None, shutter open 0–1, sky colour, sky strength, exposure
    1: ('22:00', (1.6, '#ffa560'), NIGHT, 0.25, '#2a3a66', 0.6, 0.7),
    2: ('', (0.0, '#ff9a4a'), None, 0.0, '#0d1226', 0.3, 0.6),
    3: ('03:12', (0.0, '#ff7a2a'), None, 0.0, '#0d1226', 0.3, 0.6),
    4: ('06:14', (0.7, '#ff9a55'), DAWN, 0.35, '#e9a77a', 0.9, 0.3),
    5: ('06:16', (2.2, '#fff1e2'), DAWN, 0.70, '#f6d3b0', 1.4, 0.0),
}

def mat_room():
    MATS['oak'] = bump_tex(principled('oak', srgb('#c8ad8c'), rough=0.55), 'wave', 60, 0.02)
    MATS['wall'] = bump_tex(principled('wall', srgb('#e7e2da'), rough=0.95), 'noise', 300, 0.05)
    MATS['floor'] = bump_tex(principled('floor', srgb('#b9a184'), rough=0.6), 'noise', 200, 0.03)
    linen = principled('linen', srgb('#e9e5de'), rough=0.95); b = linen.node_tree.nodes['Principled BSDF']
    b.inputs['Sheen Weight'].default_value = 0.4
    MATS['linen'] = bump_tex(linen, 'noise', 900, 0.25)
    MATS['linen2'] = bump_tex(principled('linen2', srgb('#cfc9bf'), rough=0.95), 'noise', 900, 0.25)
    MATS['shade'] = principled('shade', srgb('#f1ece4'), rough=0.9)
    sh = MATS['shade'].node_tree.nodes['Principled BSDF']; sh.inputs['Transmission Weight'].default_value = 0.2
    MATS['frame'] = principled('frame', srgb('#d9d6d0'), rough=0.5)
    MATS['slat'] = principled('slat', srgb('#cfccc6'), metal=0.3, rough=0.4)
    skin = principled('skin', srgb('#d8a689'), rough=0.55); sk = skin.node_tree.nodes['Principled BSDF']
    sk.inputs['Subsurface Weight'].default_value = 0.25; sk.inputs['Subsurface Radius'].default_value = (0.01, 0.004, 0.002)
    MATS['skin'] = skin

def bedroom_scene(n):
    t, (lamp_w, lamp_c), ring, shut, sky, sky_s, expo = ROOM[n]
    mat_room()
    MATS['led_under'] = emit('led_under', srgb(ring), 900.0) if ring else principled('led_under', srgb('#141416'), rough=0.6)
    MATS['dots'] = emit('dots', srgb('#ffd9a0'), 2.5 if n == 3 else 7.0)
    base = build_base(with_time=bool(t), time=t or '06:30')
    # nightstand: light oak, 460 × 380 × 500 mm, the base 110 mm from its front edge
    link('stand', rbox_bm(0.46, 0.38, 0.50, 0.004, 0.003, sp=4, se=2), 'oak', (0.02, 0.03, -0.50), smooth=False)
    rbox('drawer_gap', 0.44, 0.002, 0.003, 0.0, 0.0, 'cavity', (0.02, -0.161, -0.13), sp=1)
    # room: floor, back wall with a window behind the nightstand, the sky outside
    plane('floor', 6.0, (0, 0, -0.50), (0, 0, 0), 'floor')
    wall_l = rbox('wall_l', 2.4, 0.04, 2.6, 0, 0, 'wall', (-1.25, 0.39, -0.50), sp=1)
    wall_r = rbox('wall_r', 1.6, 0.04, 2.6, 0, 0, 'wall', (1.40, 0.39, -0.50), sp=1)
    wall_b = rbox('wall_b', 0.6, 0.04, 0.45, 0, 0, 'wall', (0.30, 0.39, -0.50), sp=1)
    wall_t = rbox('wall_t', 0.6, 0.04, 0.95, 0, 0, 'wall', (0.30, 0.39, 1.15), sp=1)
    for nm, w, h, loc in (('frm_l', 0.03, 1.2, (0.015, 0.37, -0.05)), ('frm_r', 0.03, 1.2, (0.585, 0.37, -0.05)),
                          ('frm_b', 0.6, 0.03, (0.30, 0.37, -0.05)), ('frm_t', 0.6, 0.03, (0.30, 0.37, 1.12))):
        rbox(nm, w, 0.03, h, 0, 0, 'frame', loc, sp=1)
    skyp = plane('sky', 3.0, (0.3, 1.2, 0.6), (math.pi / 2, 0, 0), 'sky'); MATS['sky'] = emit('sky', srgb(sky), sky_s)
    skyp.data.materials.clear(); skyp.data.materials.append(MATS['sky'])
    # roller shutter in the window: slats from the top down to how far it is open
    top, bot = 1.12, -0.05; edge = top - (1 - shut) * (top - bot) if shut < 1 else top
    z = top - 0.04; k = 0
    while z > bot + (top - bot) * shut - 0.001 and z > bot:
        rbox(f'slat{k}', 0.54, 0.012, 0.038, 0.0, 0.003, 'slat', (0.30, 0.40, z - 0.038), sp=1, se=1); z -= 0.04; k += 1
    # bed to the left: headboard, mattress under a linen duvet, a pillow
    rbox('headboard', 1.7, 0.08, 0.95, 0.03, 0.02, 'linen2', (-1.12, 0.33, -0.50), sp=6, se=3)
    rbox('mattress', 1.6, 2.0, 0.24, 0.04, 0.03, 'linen', (-1.12, -0.72, -0.24), sp=6, se=4)
    rbox('duvet', 1.66, 1.55, 0.06, 0.08, 0.03, 'linen', (-1.12, -0.95, -0.01), sp=8, se=4)
    rbox('pillow', 0.62, 0.40, 0.13, 0.08, 0.05, 'linen', (-0.62, 0.07, 0.0), sp=8, se=5)
    # lamp on the nightstand (the smart bulb) and the scent diffuser
    cyl('lamp_foot', 0.045, 0.014, 'alu', (0.15, 0.13, 0.007), seg=64)
    cyl('lamp_stem', 0.005, 0.24, 'alu', (0.15, 0.13, 0.134), seg=24)
    shade = cyl('lamp_shade', 0.075, 0.12, 'shade', (0.15, 0.13, 0.31), seg=96)
    if lamp_w > 0:
        L = bpy.data.lights.new('bulb', 'POINT'); L.energy = lamp_w; L.color = srgb(lamp_c)[:3]; L.shadow_soft_size = 0.03
        o = bpy.data.objects.new('bulb', L); col.objects.link(o); o.location = (0.15, 0.13, 0.31)
    dif = build_diffuser(); dif.location = (-0.14, 0.10, 0.0); dif.rotation_euler = (0, 0, math.radians(-20))
    # outside light through the window
    if shut > 0:
        area('window', (0.30, 0.60, 0.55), (0.0, -0.4, 0.0), 0.55, 60 * sky_s * shut, srgb(sky)[:3])
    world(srgb('#0a0c14' if n in (2, 3) else '#1a1820'), 0.05)
    if n in (2, 3):                                        # night: a faint cool light, the room is still readable
        area('moon', (-0.9, -1.2, 1.4), (0, 0, 0), 1.6, 4.0, (0.62, 0.70, 1.0))
    # the hand from the bed
    if n == 1:
        F = Vector((1, -0.15, -0.35)).normalized()
        br = build_bracelet(0.075); br.rotation_euler = (0.5, 0.2, 0.6)
        hand, _ = build_hand('pinch', basis(F, Vector((0, 0.3, 1))), Vector((-0.12, -0.02, 0.13)))
    if n == 5:
        F = Vector((1, 0.18, 0)).normalized(); R = basis(F, Vector((0, 0, 1)).cross(F))
        L_ = Vector(HAND_TIPS['palm']['index']).x
        wrist = Vector((0.05 - L_, -0.01, 0)) ; wrist.z = TOP - palm_z('palm')
        hand, _ = build_hand('palm', R, wrist); wrist.z += rest_on_top(hand)
    look((0.85, -1.30, 0.78), (0.0, 0.06, 0.06), 70, 2.8)
    scene.view_settings.exposure = expo
