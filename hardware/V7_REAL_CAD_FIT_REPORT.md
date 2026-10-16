# v7 — real supplied STEP assembly and mechanical fit work

**Disposition:** Digitally improved true-CAD fit prototype. Not production-certified; PR #3 remains draft.

## Selected actual CAD, not proxies
- **Main board:** imported original **Elecrow `00-2-13_view_asm.stp`** (28.3 MB, **240 STEP solids**); native model overall **31.268 × 10.653 × 65.978 mm**. The 10.65 mm vertical extent of the assembled board explains why the old 13.4 mm-deep case failed to leave room for the cell.
- **LiPo:** actual **Adafruit 1578** `adafruit_1578_500mAh_battery.step`, **36 × 29 × 4.75 mm**. Per owner direction, connector mismatch is **not a blocker for mechanical enclosure volume**, although it remains an electrical integration consideration.
- **Microphone:** selected **`paulrenzi__bought_inmp441.step`**, which imports as **16 × 14 × 2.02 mm**, matching the part specification exactly. Actual purchased breakout brand still unconfirmed.
- **Motor:** actual **`LCM1027A2445F_1027_coin_vibration_motor.step`**, **10.8245 × 3.3281 × 15.9125 mm including leads/contacts**. The file parses correctly in OpenCascade; earlier GitHub text decoding failure was not a damaged CAD solid.
- **Haptic-driver alternative:** actual **SOT-23 and SOD-323 package STEP files** from the provided inventory are used as the selected discrete component packages; the mislabeled SEN-11574 pulse-sensor model is excluded. No actual assembled driver PCB CAD exists, so do not claim its placement validated.

## Actual mechanical changes
- New independent source **`hardware/the_scribble_v7_real_fit.scad`**; v5/v6 retained as reference history.
- Case **46 × 82 × 20.0 mm** (rear 14.4, bezel 5.6), up from 46 × 82 × 13.4 mm.
- In real STEP assembly trial board moves **+5.3 mm Z** from v6, while the cell shifts **+2.5 mm Y / −0.2 mm Z**. This provides >0.5 mm vertical gap between their **complete vendor envelope bounds** and 0.5 mm Y gap between battery and full wired motor model.
- Enlarged motor retaining ring bore to **11.6 mm** and OD to **13.8 mm**, with **inboard +Y wire lead relief** based on the actual manufacturer shape.
- Rear buttresses, actual openings, bezel glass/board pocket, snap head positions and button guides shifted to correspond with the deeper board position.
- **Bezel pocket 32.0 × 66.6 mm** extending to z18.75; extra roof thickness retains approximately 1.25 mm above the pocket.

## Verification evidence (October 16, 2026)
**Native B-rep assembly, zero substitutes:**
- Remote GitHub Actions run: https://github.com/pauldavid1974/the-scribble/actions/runs/38950913393
- Source-cad loader: `hardware/audit_source_step.py`; assembly/intersections: `hardware/assemble_real_step.py`.
- Entire actual CrowPanel assembly, cell, chosen INMP441, motor, SOT23 and diode imported successfully.
- **Every native model pair in the revised v7 assembly has zero intersecting AABB volume** (conservative geometrical proof that their solids cannot overlap). The earlier v6 actual B-rep test had board/cell **110.546 mm³** and battery/motor **1.374 mm³** interferences; these are resolved by the revised positions.
- Local OpenSCAD full CGAL renders: rear = **1 watertight solid**; bezel = **1 watertight solid**; actuator caps = **3 watertight solids**; no rest-position control penetration reported.
- Tessellated **actual vendor CAD surface point classification** using VTK against the authoritative rendered OpenSCAD rear and bezel: **0 enclosed points** for the battery (96 vertices), motor (4,258 vertices), microphone (1,284 vertices), and **20,000 sampled board vertices** against each shell. The initial v7 bezel yielded 108 sampled board vertices embedded in the shell; enlarging the **actual glass/board pocket** eliminated these sampled intersections. **This is a sampled surface test, NOT a complete native STEP-to-case-solid Boolean.**

## Remaining required checks
1. Validate USB-C mating cable insertion and exact PCB/STEP coordinate registration with hardware.
2. Establish bottom-port position and sealing foam ring alignment on the chosen microphone breakout.
3. Verify top tactile switch/button movement, rocker actuation, snap print tolerances and lid seating on a physical trial print.
4. Determine the final real haptic driver mounting (discrete packages vs an actual assembled driver PCB); current SOT23/diode packages alone don't establish a PCB.
5. For final manufacturing signoff, run exhaustive case-to-parts surface/volume interference or actual printed assembly test. Exact electrical connector selection is **out of scope for the enclosure packaging gate** per owner's instruction.

Do not interpret a GitHub CI pass or the old v6 viewer as a physical fit certificate. Use the **native STEP assembly** from the workflow artifact or download package for genuine source-CAD inspection.

### Final exact-revision CI result

- **GitHub workflow run 38950913393: PASS.** OpenCascade imported actual source STEP solids, assembled the revised real-part model, and reported zero pairwise intersections by proven disjoint 3D solid bounds.
- Authoritative OpenSCAD rendering on the GitHub runner: `rear` = 1 watertight body, `bezel` = 1 watertight body, `side_caps` = 3 independently watertight pieces, `print_layout` = 2 watertight print-placement bodies. All STL meshes generated directly from `hardware/the_scribble_v7_real_fit.scad` on the reviewed branch; no viewer export masquerades as print CAD.
- Download native STEP, original vendor STEP files, and printable STLs as the three artifacts attached to [this successful run](https://github.com/pauldavid1974/the-scribble/actions/runs/38950913393).
- The **physical print, actual controller button travel, audio-path alignment, complete driver circuit board, and exhaustive case-solid-to-STEP Booleans remain unverified**. This is a valid digital prototype, not a certified production enclosure.
