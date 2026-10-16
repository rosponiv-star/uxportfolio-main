# 03 · Smart Home Hub — facts

Source: `Media/03-Smart Home Ecosystem/REPORT FINALE PIG.pdf` (172 slides, Italian). Course "Progettazione di Interfacce
Grafiche" (PIG), a.y. 2025/26. Team: Valerio Rosponi, Marco Scognamiglio, Giorgia Pajola (3).

## Brief
- Domain: home automation. Software for a (hypothetical) partner company that makes, sells, installs and services the
  hardware. The app only manages devices already installed: no sales, installation or hardware support (non-negotiable).
- Value proposition: one app for every device in the house, so the partner stands out and customers add more devices
  (loyalty, upgrades).

## Stakeholders
- Primary: owners/household (parents, adult children); delegates with limited access (babysitter, home carers,
  cleaners).
- Secondary: young children; maintenance technicians; outsiders who interact with the house (guests, couriers,
  acquaintances); the wifi provider.
- Tertiary: the partner company.

## Domain modelling (Diamond 1)
- Domain map, artifact model (+ artifacts per action/situation), sequence & flow models with **touchpoints** (borrowed
  from service design), physical model.
- 8 sequence/flow models selected: enter the house, leave the house, switch an environmental device on/off, cleaning
  and mowing, opening the door to guests, burglars break in, fire.
- **16 pain points**, **6 personas** (4 primary + 2 secondary): Marco (businessman always in a rush, wants a house that
  "runs itself"), Giorgia (absent-minded artist, forgets lights/keys/deliveries, feels unsafe alone), Valeria (caring
  mum, kids + babysitter + pets), Noemi (daughter, secondary, afraid of being alone in the evening), Franco
  (independent grandfather, mobility issues, distrusts leaving keys/codes), Gianni (Amazon courier, secondary: no way
  to reach whoever is home).
- Persona photos look AI-generated; no interviews/survey are mentioned in the report.

## Pain points (counts = personas affected)
pp01 forget keys/remote (2) · **pp02 forget to arm/disarm the alarm (2)** · **pp03 not home when the intercom rings (5)** ·
pp04 not knowing who is home (2) · pp05 keep an eye on kids and pets (1) · **pp06 not knowing if something was left
on/open (4)** · **pp07 giving keys to an outsider you don't trust (2)** · pp08 house not cool/warm on arrival (1) ·
**pp09 feeling unsafe home alone (3)** · pp10 can't call for help fast (3) · pp11 not wanting to give full control to
anyone with the app (1) · pp12 forgetting alarm/door codes (1) · pp13 no time for cleaning/garden (3) · pp14 walking
difficulties (1) · **pp15 not hearing the intercom (3)** · pp16 opening to strangers unknowingly (2).
Tackled (bold): 02, 03+15 (merged: solutions converged), 06, 07, 09 → 5 design areas. Chosen by impact and recurrence.
Others solved indirectly per flow (e.g. 01, 12, 13, 14, 16, 10).

## Design brief conclusions
1. Technology creates anxiety, not only comfort: uncertainty about system state ("did I really turn off the light?");
   fragmentation raises cognitive load.
2. Trust: access for third parties (babysitter, couriers, guests) is unsolved; physical keys and shared codes feel unsafe
   → need a specific, temporary delegation system.
3. Accessibility barriers: elderly/less expert users fear "pressing the wrong button".
- Direction: **discarded the "universal remote" idea** → a **security and management hub**: visual centralisation
  (dashboard/house view), dynamic access system, **safety-first** patterns (sliders instead of toggles for critical
  actions, confirmation dialogs), "distraction-proof", usable in a hurry or with motor difficulty.

## Process (Diamond 2)
- Divergent: each of us sketched design concepts by hand on paper, per pain point and persona.
- Convergent: compared concepts in a Design Space (Figma board), grouped by pain-point affinity across personas;
  separated must-have elements from secondary ones → **happiness factors**.
- Prototypes in Figma, then UX flows; flows checked back against the sequence/flow models (does the app replace the
  touchpoint?).

## Happiness factors / features by pain point
- pp06: overview of all devices; **floor plan** of the house (devices where they are, colour per room, on = primary
  colour, off = neutral); room detail; ordered list filterable by room/category; on/off state + switch per device;
  notification of devices left on when you leave; notification + history for parents when a device is switched on
  while away.
- pp02: notification if the alarm isn't armed when you leave (arm remotely); lock-screen/home **widget** with alarm
  state + quick action.
- pp03+15: intercom rings → notification at home, **call on the phone** when away; **intercom panel**: camera video,
  hang up, push-to-talk, open gate/door; which bell was rung + suggestion of what to open; **missed intercom call**
  notification (who/where/when); **temporary codes** for couriers/guests (expire after use or time; levels: gate, door,
  parcel box); idea: shipping code auto-linked via API/e-commerce email = access code.
- pp09: security dashboard (each security device, state, switch, every window/door open or closed: can't arm with
  windows open); emergency notification + automatic call to emergency services/contacts, defence systems if away
  (smoke); one button to arm everything or pick systems; security **routines** (e.g. night) with a notification.
- pp07: personal permissions with **unique codes tied to one person** (traceable, revocable, no lock change); see when
  an outsider is expected (days, validity window); notification when a code is used.
- Automations screen (pp06+pp09 merged): device routines, quick actions ("I'm cold", "Leaving home"), security routines.

## Interface (Material Design 3)
- Sections (vertical navigation): Home (Casa), Security, Access, Automations, History.
- App bar with page title + profile/settings always present.
- Floor plan: primary tabs for floors; connected button group to show lights / devices / windows-doors; tapping a room
  filters the list. Device cards in the room's colour (MD3 presets GreenLT, BlueLT, …); subtitle = model + last
  setting (only if settable), switch on the right; card → modal bottom sheet with secondary tabs (controls vs
  settings).
- Intercom: tabs gate/door (red badge on the one that rang); **standard slider to open** (knowingly off-guideline:
  a deliberate, continuous gesture, no dialog that would interrupt the live video); floating toolbar (end call red,
  mic, speaker, torch).
- Access codes: connected buttons permanent/temporary; list items (pin, type, access level, profile); extended FAB "add";
  bottom sheet edit; menu+text field for the profile; multi-select connected buttons for gate/door; filter chips for
  weekdays; validity = permanent / single use / time window (date range picker; time pickers separately, MD3 has no
  time-range picker); "Save and activate" (primary) vs "Save without activating" (neutral).
- Security: tabs per floor; connected buttons sensors / defence / cameras; filter chips break-in vs environment;
  extended FAB "Arm alarm"; **snackbar if windows are open** (imperative: says what to do); **basic dialog to confirm
  arm/disarm, emphasis on Cancel** (harmless if pressed by mistake); cameras in a 16:9 hero carousel, border in the
  room colour; rooms without cameras look "dark" on the plan.
- Automations: buttons for quick actions, cards for routines, extended FAB to add.
- Colour roles: destructive FABs in tertiary-container (always visible, cautious but not alarming like
  error-container); destructive buttons error-container; connected buttons = primary filtering (selected secondary),
  chips = secondary filtering (outline); single vs multi select told apart by icons/checkmarks.
- Chip behaviour: in selection chips "All" selects everything visibly; in security filter chips "All" does not
  (so one tap switches filter instead of deselecting).

## Validation
- No usability testing in the report. Validation = flows checked against the sequence/flow models.

## Owner answers (2026-10-16)
- Name: Smart Home Hub. Role: all phases shared equally among the three. Personas: proto-personas, no interviews.
- Sep–Dec 2025, Android, Material Design 3, Figma + FigJam.
- Define compares Marco vs Franco. Design rows: floor plan, intercom, access codes, security (+automations).
- Stays placeholder (Coming soon) until the owner sends the interfaces. No Validate chapter.
- Shipping code via e-commerce, automatic emergency call and smoke defence: shown in Design as "Beyond the screens" (system ideas, not interfaces), owner 2026-10-16.
