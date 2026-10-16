# The Scribble — v6 enclosure fit audit (2026-10-16)

**Disposition: DIGITAL FIT PROTOTYPE, NOT CERTIFIED FOR FINAL ASSEMBLY.** Reference: [blocking issue #2](https://github.com/pauldavid1974/the-scribble/issues/2). The v5 design remains unchanged. This branch adds a new independent \`hardware/the_scribble_v6_fit.scad\` for physical fit trials.

## Exact part/CAD cross-check

| Item | CAD/reference in repo | Decision/evidence | Remaining gate |
| --- | --- | --- | --- |
| Main CrowPanel 2.13" ESP32-S3 | \`hardware/specs/board.brd\`, vendor official \`00-2-13_view_asm.stp\` downloadable with \`scripts/fetch_models.py\` | Eagle layer 20 confirms **63.2 × 31.2 mm** R1 PCB. Coordinate mapping was checked against button positions. | Register and import the actual full Elecrow STEP before claiming complete 3D electronics clearance. It is *not* in this repo. |
| Battery | \`hardware/models/adafruit_1578_500mAh_battery.step\` | Shape envelope **36 × 29 × 4.75 mm** matches [Adafruit 1578](https://www.adafruit.com/product/1578). v6 orientates 29 mm across X and 36 mm along Y. | The Adafruit product ships with JST-PH 2.0 mm, incompatible with the CrowPanel SH1.0-2P battery socket. Confirm exact protected battery and safe lead adapter/polarity before power-on; no hard cell clamping. |
| Battery mating connector | \`hardware/models/JST_SH_BM02B-SRSS-TB_..._Vertical.step\` plus SHR-02V-S/S-B plugs | **Not an acceptable exact fit match**: the Eagle B1 package is \`SH1.0MM-W\` side-entry; listed vertical JST STEP is a *different orientation*. | Obtain exact mating board-connector STEP, verify real opening toward lead end, bend radius, polarization and strain relief. |
| INMP441 microphone | Four alternative third-party INMP441 STEP files in \`hardware/models/\` | Not proven the same breakout as the eventual purchased board. Repo README says **16 × 14 × 2.02 mm**, while v5 preview erroneously assumed a Ø14 circular PCB. v6 reserves 16 × 14 × 2.02 mm. | Pick actual breakout SKU/CAD, align bottom acoustic hole and foam gasket to *its* package and PCB location, verify attached wires. |
| Coin haptic motor | \`LCM1027A2445F_1027_coin_vibration_motor.step\`; alternate 1027 shapes | [LEADER LCM1027A2445F](https://jlcpcb.com/partdetail/LEADER-1027/C2759984) is **Ø10 × 2.7 mm**, **wired/lead mount**. v6 holder has a new +X wire exit. The previously named [Vybronics VC1027B200N](https://www.vybronics.com/coin-vibration-motors/with-brushes/v-c1027b200n) is **spring-contact**, a different electrical interface. | Confirm which of these two is physically in hand and that strain relief and electrical interface suit it. Do not confuse alternatives. |
| Haptic driver | \`hardware/models/vibration_motor_module_snapmagic.step\`, labeled \`SEN-11574.STEP\` in file header | **WRONG PART**: [SparkFun SEN-11574](https://www.sparkfun.com/pulse-sensor.html) is a **pulse sensor, not a MOSFET vibration driver**. No exact selected driver assembly CAD exists. v6 reserves a conservative 12.36 × 13 mm prototype envelope only. | Specify/build actual MOSFET/diode/resistor driver PCB with known outline and pin clearance, or select exact available module with genuine STEP model. |
| Case/actuators | \`hardware/the_scribble_v5_step.scad\`, \`hardware/case_model_viewer.html\` | v5 snap centers ±13.8/±30.8 were within PCB footprint. v5 exported STL generated from viewer meshes did not make correct boolean acoustic/USB holes. | v6 places four snap centers at ±18.2/±33.5 and uses true OpenSCAD CSG; printed switch travel and retention must still be tested. |

## Fit-prototype changes

- Outer **46.0 W × 82.0 L × 13.4 H mm**; board cavity **31.6 × 63.6 mm** (0.20 mm nominal clearance each edge).
- Rear floor thickness **1.8 mm**; upper/lower split at z9.1. Board supports have full load path to shell sides.
- Spherical snap pins and matching undercut pockets outside the rectangular PCB envelope, with approx **0.75 mm** nearest head-to-PCB lateral clearance. Snap heads require physical PETG flex verification; avoid brittle material.
- USB-C plug-access notch spans both halves and provides 15.5 mm width by 6.7 mm height; depth/real cable collar needs fit confirmation.
- Rear BOOT/RESET tool holes and single central microphone acoustic through-bore genuinely cut through shell; rear gasket seat is a *real* raised ring.
- Non-overlapping floor zones for battery, mic, wired Ø10 motor, and a nominal driver PCB. The motor holder now has a wire-exit notch.
- Three separate trial button plunger/rocker pieces, **not yet qualified for switch feel, electrical contact or ±2.3 mm rocker stroke**. They are prototypes to fit-test, not claims of finalized switch actuation.

## Digital evidence collected

OpenSCAD CGAL rendered to exported STL. Python \`trimesh\` inspection:
- \`rear.stl\`: **1 connected component; watertight**.
- \`bezel.stl\`: **1 connected component; watertight**.
- \`side_caps.stl\`: **3 independent connected, watertight print pieces**, all based on z=0.
- \`print_layout.stl\`: **2 independent connected, watertight parts**, on printer bed (rear and inverted bezel).
- Digital CSG shell/envelope intersection: **no positive-volume interference** with nominal PCB, glass, motor, battery, mic, and prototype-driver envelopes. The rear check produced only zero-thickness coincident contact faces where the PCB is intended to rest on support tabs. Bezel check was empty.
- Rest-position button/shuttle CSG intersection against rear shell: **empty**.

These are checks against **explicit simplified envelopes**, *not* full registered vendor STEP BREP solids. They do not prove fit of real connector housings, protruding component pins, motor wiring, acoustic response, battery lead bend, cap retention strength, or print process tolerances.

## Reproduce with OpenSCAD

\`\`\`bash
openscad -o rear.stl -D 'part="rear"' hardware/the_scribble_v6_fit.scad
openscad -o bezel.stl -D 'part="bezel"' hardware/the_scribble_v6_fit.scad
openscad -o side_caps.stl -D 'part="side_caps"' hardware/the_scribble_v6_fit.scad
openscad -o print_layout.stl -D 'part="print_layout"' hardware/the_scribble_v6_fit.scad
openscad -o rear_clash.stl -D 'part="rear_clash"' hardware/the_scribble_v6_fit.scad
openscad -o bezel_clash.stl -D 'part="bezel_clash"' hardware/the_scribble_v6_fit.scad
openscad -o buttons_clash.stl -D 'part="buttons_clash"' hardware/the_scribble_v6_fit.scad
\`\`\`

For the three \`*_clash.stl\` files, genuinely empty geometry or a zero-volume coplanar support-touch result is expected. Any positive-volume intersection is a stop condition.

## Before accepting

1. Use the *actual* vendor STEP and real purchased board/mic/motor/driver/battery models, fix coordinate transforms, and repeat solid interference analysis. Explicitly retire misleading third-party STEP names.
2. Print a cheap shell/bezel fit prototype; measure mounting, top controls (including center rocker full travel), snap force and fatigue, actual USB cable collar, screw-free board capture, sound-path gasket seal and 2.4mm BOOT/RESET access.
3. Verify SH1.0 battery wiring and polarity before attaching LiPo; do not pierce, compress or alter the cell pouch. Verify the haptic driver's components and wiring.
4. Refine tolerances for the actual printer/filament, then run final watertight/slicer checks and a full assembly test.

**Do not merge and label v6 production-ready solely based on this document.**
