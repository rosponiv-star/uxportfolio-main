# 02 — Rehab → "Rehabeat" (notes from Media/02-Rehab)

Sources: `old-portfolio-rehab.pdf` (old portfolio page, 1 long page) = OLD; `hci.pdf` (project report, 58 pages) = HCI.
Page refs: HCI pN.

## OLD portfolio page (title then: "Rehabilitation System")
- Tagline: "A UX concept grounded in research on the role of music in sports rehabilitation for amateur athletes
  recovering from injuries."
- Overview: home-based digital rehabilitation ecosystem integrating precision sensors, AI and rhythmic-musical feedback.
  For amateur athletes; bridges professional clinical supervision and domestic autonomy.
- Challenge: post-injury recovery is fragmented → incorrect execution and therapy abandonment. Replicate the
  "vigilant presence" of a physical therapist at home.
- Outcome: connected fitness platform fusing AI vision + wearable sensors; real-time "Digital Twin" on the user's TV
  for instant form correction.
- Team: four design students. Role: End-to-End UX Designer. Client: faculty-led university project.
  When: October 2024 – January 2025.
- Problem framing: home rehab relies on static paper protocols or generic video tutorials; no feedback loop (user can't
  know if they perform correctly). Repetitive, solitary → rapid decline in protocol adherence, longer recovery,
  burden on healthcare system.
- Research target: amateur athletes in post-injury recovery, 18–50 y/o.
- Research approach: Lean UX; discovery prioritised clinical literature + established physiotherapy protocols over broad
  qualitative testing; plus heuristic evaluation of existing fitness apps (safety gaps in unsupervised environments).
  "Secondary Research & Heuristic Analysis".
- Key insights: (1) "The anxiety of blind execution": abandonment driven by cognitive uncertainty, not physical
  capability; "feedback vacuum"; can't verify posture → kinesiophobia (fear of re-injury) → hesitant movements.
  (2) "The burden of the clinical stigma": home exercises seen as passive medical obligation, reminder of injury, not a
  training challenge; "patient mindset" strips gratification; no progression/reward → frustration → drop-off.
  Conclusion: visual validation converts anxiety into safety; rhythmic structure (music) shifts passive endurance to
  active performance. "Replace the guesswork with evidence and the silence with flow."
- Archetypes (from physiotherapy protocols and patient adherence data):
  01 The Anxious Perfectionist — Kinesiophobia. Quote: "I want to recover, but I am terrified of making a wrong move and
     hurting myself again." Pain: insecurity in execution; constant need for reassurance. Needs: certainty of moving
     correctly. Opportunities: real-time visual feedback; postural correction (sensor tracking).
  02 The Bored Achiever — Boredom. Quote: "I know what I have to do, but repeating the same exercises in silence is
     demotivating." Pain: loss of stimulus; sees therapy as tedious "chore". Needs: rediscover the joy of movement;
     sense of athletic challenge. Opportunities: musical gamification; rhythmic sync to drive the flow.
- Design principles (3 pillars): Clinical precision, home comfort; Rhythmic flow (music as functional driver, BPM
  dictates execution speed); Visual feedback loop ("augmented digital mirror" overlaying instructions on reflection).
- Solution: distributed system, three synchronised touchpoints:
  1. The Hub: mobile app — medical data ingestion, AI-driven plan configuration, long-term progress monitoring.
  2. The Guide: TV interface — connected to smartphone, training space: guide avatar, real-time correction, metrics.
  3. The Tracker: sensor integration — inertial hardware (e.g. Euleria Health technology) + computer vision; gyroscopic
     sensors + smartphone camera → skeletal map, angular micro-errors.
- UX phases: 01 Biometric calibration (age, gender, weight, height → biomechanical model, load limits, range of motion);
  02 Clinical data to rehabilitation plan (upload medical report, OCR + NLP → periodized plan aligned with physician);
  03 TV connection (phone → TV); 04 Gyroscopic sensor connection (pair sensors, orientation, count reps).
  App UI language in old screens: Italian.
  03 TV connection: Wi-Fi phone–TV, QR code or numeric code ("Connetti il tuo Smartphone"); instructions visible from a
     distance. 04 Inertial sensors: Bluetooth, search → "Sensore trovato" → confirm; count reps.
  05 Adaptive music selection: acoustic profile → track per exercise, music BPM synced to target movement cadence;
     "Best Fit" track preloaded; user can override (choose song, e.g. "Da 60–70 Bpm", tabs Preferite/Consigliate/
     Popolari). Example screen: "American Dream – 21 Savage, 69 bpm", "Squat gamba singola", "Durata allenamento 1 ora".
  06 Setup & positioning: phone placed below the TV, camera sees workout area; presence + framing check; visual cue
     confirms readiness (green "Mantieni la posizione" / red when wrong); a gesture triggers countdown.
  07 Active execution & real-time biofeedback: immersive gamified interface "inspired by rhythm-based motion platforms";
     optical tracking (phone camera) + gyroscopic sensors → live "Digital Twin" avatar on TV mirroring movements,
     side-by-side with instructor; AI monitors biomechanics, overlays real-time corrections (red chevrons) on the avatar.
     TV shows song + bpm, exercise name + reps ("Pollice in su x10", "Flessione gamba x10"), progress bar.
  08 Weekly progress insight: weekly summary integrating sensor data (range of motion improvement, stability scores)
     + post-workout questionnaires (perceived effort); compare; AI recalibrates difficulty for next cycle.
     Screens: "Congratulazioni! Hai superato la prima settimana", expected vs reached curve, "Ripresa generale 25%",
     "Riduzione del dolore 65%", "Ripresa forza 30%", "Ripresa mobilità 55%" (MOCK UI DATA, not research results).
- Projected impact (old page, all qualitative, no numbers): operational optimisation (fewer check-up visits, therapists
  focus on acute cases, scalable/cost-effective); psychological activation (gamification → adherence; "treating
  illness" → "rhythm of movement"); biomechanical fidelity & safety (form deviations detected in real time);
  data-driven progress quantification (ROM, stability scores + questionnaires → validates protocol efficacy).
- Old visual style: dark UI, purple/indigo gradients, iPhone + TV (Studio Display-like) mockups.

## HCI report (hci.pdf, Italian, 58 pp.)
- p1–2: "Progetto HCI — Interazione Persona-macchina con elementi di comunicazione multimodale", University of Trento.
  Team: Leoni Alessandro, Lisci Nicolò, Rosponi Valerio, Scognamiglio Marco. (≠ JustCook team except Marco.)
- Report structure (Design-thinking style): 1 Comprendere (problem definition, team) · 2 Osservare (research:
  human backgrounds, product backgrounds) · 3 Punto di vista (PDS definition) · 4 Ideare (define the system, develop it).
- p2 (report page 2) Problem: rehabilitation of amateur athletes after injury, especially those who want to return to
  training and strengthen the injured area. Goal: monitor the recovery process closely so athletes keep practising
  their sport while minimising risks. Explore solutions to support a safe return to sport.
- Team skills (report p3): Leoni — IT, problem solving; Lisci — IT, lexical, organisational; Rosponi — graphic, IT;
  Scognamiglio — IT, planning.
- Report p5–6 "Human backgrounds" (desk reasoning, NOT field research):
  1.1 Client needs: keep injured area trained via targeted exercises; execute exercises correctly (avoid further
  damage) → gyroscopic sensors give precise feedback on movement quality; monitor progress after each session
  (efficacy + motivation); a programme designed to minimise consequences; understandable and manageable without
  constant doctor supervision; from a professional medical report an app can generate a personalised programme and
  present recovery data clearly.
  1.2 Client problems: poor knowledge of rehab practice (don't know how to proceed) → app with personalised, easy
  exercises; lack of motivation (concentration, will) → music or rhythm-based exercises; lack of specific exercises
  for particular injuries/body parts → AI generates targeted programme from the medical report; uncertainty about
  recovery state → frustration → clear regular feedback after each session.
- Report p6 "Product backgrounds — similar products": Euleria (Euleria Health): platform for movement professionals,
  rehab in clinic or remote; sensors give precise progress data; gamification for motivation; each patient followed
  by a specialist. Many injury types (movement, cardiac, cognitive). Downsides: needs a professional first to define
  the plan; not usable autonomously by patients; data hard to interpret for non-experts; needs constant expert support.
- Report p8–11 "Punto di vista — Definizione PDS" (Point of view / problem definition statement):
  Target: amateur athletes, men and women of ANY age (old page says 18–50), who after an injury want a safe rehab path
  and to monitor progress from home; motivated to return to sport; busy daily lives; need effectiveness, simplicity,
  accessibility; minimise frequent medical visits / trips to specialised centres.
  Needs: manage rehab autonomously at home (save time/resources); targeted exercises for the injured area without
  worsening it; correct execution — precise feedback on movements, correct errors in real time; clear progress
  reports; a structured programme without constant doctor supervision: from an initial medical report, a personalised
  autonomous plan with understandable data/instructions.
  Problems: poor rehab knowledge (which exercises, intensity, how long) → uncertainty, delays; lack of motivation and
  focus (monotonous, boring) → abandonment or inconsistency; generic programmes not targeted to specific injuries →
  slow/incomplete recovery, higher relapse risk; hard to assess own progress → frustration, feeling lost.
  2 Main goals: safe, personalised, motivating path; correct execution, continuous monitoring, detailed feedback;
    motivational elements like syncing exercises with music are central.
  3 Technical: gyroscopic sensors + smartphone camera monitor and correct posture; AI analyses data, immediate
    corrections, adapts programme WEEKLY. Smartphone app central; sync with TV/monitor shows instructions, a guide
    silhouette ("sagoma guida") and real-time feedback.
  4 Importance of music: "music is the heart of the system"; each exercise synced with tracks selected by AI per
    movement type and required rhythm; more pleasant + unconscious learning of movements, like dance (steps memorised
    through rhythm); helps focus, fewer distractions; choose favourite genre → personalisation; keeps consistency.
  5 Social contribution: fewer frequent medical visits → optimise healthcare time/resources, relieve the health system;
    accessible alternative for those who can't attend physio centres or get constant support; psychological
    wellbeing: from tiring chore to pleasant experience, less stress, less solitary.
- Report p13 "Ideare — Definire il sistema": aim: a digital environment that replicates, personalised and accessible,
  a physiotherapist's supervision. Wearable sensors + AI + interactive app; safe, effective, motivating, from home.
  Components (3): 2.1 Smartphone app (core: configure, manage, monitor; collects sensor data, analyses in real time) …
- Report p14–16: 2.2 TV: main visual support, connected via Bluetooth or Wi-Fi; instructions, virtual avatar,
  real-time feedback; lets user focus without distractions. 2.3 Wearable gyroscopic sensors: track movements precisely,
  work with the phone camera for accurate data → immediate feedback + progress. "Simple to use even for people not
  familiar with technology."
  3 How it works: 3.1 Plan creation: user uploads the medical report (injury, area, professional's recommendations);
  AI generates a targeted plan; plan adapts dynamically: if the weekly report shows exercises weren't effective, AI
  updates the plan. 3.2 Preparation: switch on phone, sensors, TV; connect via Bluetooth/Wi-Fi (connections
  remembered); app guides placing the phone under the TV facing the user; framing shown on both screens to check
  distance; system confirms automatically when ready. 3.2 Execution: "Comincia allenamento" button; TV is the focal
  point: virtual avatar reproducing movements in real time (sensors + camera), guide silhouette showing correct
  execution, immediate feedback on posture/movement errors with suggestions. Phone keeps camera framing; pause/stop
  button, also via gestures detected by the camera. 3.2.1 Personalised music: each exercise synced with an AI-chosen
  track per required rhythm; user can pick other tracks compatible with the needed BPM.
  3.3 Weekly monitoring: detailed report in the app: workout completion, physical improvements in clear charts,
  analysis of plan efficacy; if not effective → automatic changes: more specific exercises, intensity/duration
  changes, adaptations based on sensor data and physical reaction. 3.4 Tailored system: continuous support that
  evolves with the user; "followed step by step to full recovery".
- Report p17 System map: User —wears/uses→ Sensors (gyroscopic bracelets, "Pedana" = a floor mat/board) —WiFi→
  Smartphone app —WiFi→ TV app; TV gives video/audio feedback to user; app gives feedback & progress; interaction.
- Report p18 User flow map (dense diagram: sign-up/login, data, home, upload report, confirm data, plan, TV pairing
  QR/code, devices, music choice, workout, questionnaire, details/progress, profile/settings).
- Report p19+ "Sviluppare il sistema": UI screens (Italian, dark purple), starting with Entra/Registrati.
- Report p19–54: UI screens only (no text). Phone: sign up/login (email, Google, Apple), body data (sex, weight,
  height, age on a silhouette), "no programme yet → upload report", upload medical report (PDF), confirm extracted data
  (reason, results, conclusion — editable), generating plan with AI, weekly plan (weeks, days, today's workout, exercise
  carousel, duration), settings/profile (avatar, weight, height), plans (current/past), devices (sensors, TV), pair
  sensors (searching/found/failed), weekly congratulation + charts, details (general recovery, pain reduction, strength,
  mobility), pain detail, pair TV (QR/code), music (best fit track with bpm, choose song from 60–70 bpm, search),
  position phone, framing green/red, gesture "thumbs up to start", POST-WORKOUT QUESTIONNAIRE (sliders 1–10: pain felt,
  fatigue felt, how hard was the workout, how much mood improved) → "Conferma risposte".
  TV: "Connetti il tuo Smartphone" (QR + numeric code), loading, "Ciao Anna!", position phone, framing green ("Mantieni
  la posizione") / red, "Pollice in su per cominciare", workout with avatar + guide silhouette + song/bpm + exercise
  name, red chevrons on error, countdown "Prossimamente… 20" next exercise, "Allenamento completato! Congratulazioni!
  Ora compila il questionario sul telefono".
- Report p55 "Interfaccia analogica": the sensors are bands (chest/arm strap, image = heart-rate-strap style) that detect
  movements precisely and work with the phone camera.
- NO user research with real people, NO usability testing, NO numbers/statistics anywhere in the report or old page.
  Research = desk reasoning + one competitor (Euleria). The "Lean UX / clinical literature / heuristic evaluation /
  adherence data" claims appear ONLY on the old portfolio page, not in the report → ask owner.
- Name in report: none ("il sistema"). Old page: "Rehabilitation System". New name (owner, 2026-10-09): "Rehabeat".

## Owner answers (2026-10-09)
- Name: Rehabeat. Research: desk research + clinical literature/physio protocols + heuristic review of fitness apps
  (don't name the apps). Euleria = a REFERENCE, not a real competitor. Role: End-to-end UX designer.
  Tools: Figma, FigJam. Year on card: 2024; timeline Oct 2024 – Jan 2025. Type: "Connected health system".
  Archetypes: keep, flagged as synthesised from the research. Result numbers: system facts ("The system").
  Reflection: test with real users; involve a physiotherapist from the start; verify the music/BPM idea.
  Stays "Coming soon" (placeholder: true) until the real interfaces arrive. No UI from the report: placeholders.
  Literature numbers allowed in Challenge, with sources.

## Literature (verified 2026-10-09)
- Ardern, Taylor, Feller, Webster (2014), Br J Sports Med 48(21):1543–1552. 69 articles, 7,556 participants after ACL
  reconstruction: 81% return to some sport, 65% to pre-injury level, 55% to competitive sport. Positive psychological
  response favoured return to pre-injury level. https://bjsm.bmj.com/content/48/21/1543
- Argent, Daly, Caulfield (2018), JMIR mHealth uHealth 6(3):e47 (viewpoint): non-adherence to home exercise as high as
  50%; 30–50% in musculoskeletal cohorts. https://pmc.ncbi.nlm.nih.gov/articles/PMC5856927
- Terry, Karageorghis, Curran, Martin, Parsons-Smith (2020), Psychological Bulletin 146(2):91–117: meta-analysis of 139
  studies, 3,599 participants: music → better affect (g=0.48), performance (0.31), lower perceived exertion (0.22).
