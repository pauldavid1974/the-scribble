# v8.3 rotary-wheel edge-slot correction — source CAD evidence

The v7 enclosure **could not operate the stock TM_2024A rotary switch** because it inserted a printed sliding control over a toothed wheel, and the wheel was recessed ~8 mm behind the case end. v8 replaces that arrangement instead of modeling a false switch.

## Evidence from original Elecrow STEP

The original Elecrow CrowPanel `00-2-13_view_asm.stp` imported as 240 source solids. Individual solids directly contain:

- Rotary switch assembly: X=**−6.582..+6.582**, Y=**23.988..32.981**, Z=**13.152..15.952** mm in the v7 assembly coordinate frame. It has a curved toothed rim, not a linear actuator.
- Left MENU/EXIT pushbutton tips: X=**−12.65..−9.65**, Y=**29.538..31.038**, Z=**12.860..14.360**.
- Right pushbutton tip: X=**9.65..12.65**, Y=**29.538..31.038**, Z=**12.860..14.360**.

(The geometry is measured after transforming the vendor's 3D STEP into the v7 case reference frame. These are *source STEP solid* bounds, not nominal proxy boxes.)

## V8 package changes

- Translate the entire board/whole official STEP assembly **+7.0 mm Y** toward the short end, not an individual simulated switch.
- The rotary rim now extends to **Y39.981**, only **1.019 mm inside** the case's top Y41.0 boundary.
- Replaced the oversized front-bezel U-shaped scallop with a **14.2 mm wide × 3.9 mm high rounded capsule slot through the short end of the enclosure**. Its axis is at Z14.55; it extends inward 6.0 mm from Y42.0. A shallow tapered outer bevel widens the exposed mouth without opening the front-bezel roof. This keeps the green circuit board covered while exposing the real toothed rim from the top edge.
- Remove the artificial center sliding/rocker cap **entirely**. The original switch remains fixed to its factory PCB.
- Reposition the display/PCB pockets, active display window, USB opening and BOOT/RESET holes along with the board.
- Refine the independent two button plungers: their resting inside face is at Y38.150, ~**0.112 mm** in front of real switch contact tips at Y38.038. Their outer faces stop at Y40.85 (0.15 mm inside the outside wall), preserving **0 mm top-edge overhang**.
- Preserve 46 × 82 × 20 mm enclosure outer envelope.

## Checks performed, and their limitations

1. OpenSCAD **CGAL** exported rear, bezel and side-cap STL geometry successfully. All three meshes are **watertight**. Rear and bezel each form one connected body; side caps produce exactly two.
2. **Actual** Elecrow STEP wheel meshes (8,455 sampled vertices), real button meshes (1,224 vertices each), and a wider 25,000-vertex sampling of the full actual CrowPanel assembly translated +7 mm were each compared against the OpenSCAD rear and bezel using VTK point-in-solid checks; **zero sampled model vertices lie inside the case solids**. Battery, motor and microphone mesh vertices also showed zero case penetrations.
3. Real pushbutton cap meshes were checked against both stock switch source solids at rest; **no sampled cap vertices lie in either actual key's solid**.
4. The viewer in `hardware/case_model_viewer.html` embeds source STEP-derived models with the real dial isolated and an **Inspect wheel** focus control. It is a phone-friendly, offline HTML model, not a source of printable solids.

**Important:** Static CAD surface-point clearance does **not** establish dynamic wheel rotation, spring return, push-to-click stroke, finger comfort, full-surface mesh collision, or print tolerance. The official STEP represents the switch as a single solid, so the moving wheel's precise rotation range is **not modeled as a separate rigid component**. This remains a fit prototype requiring real control test. The driver PCB is still unselected, and the battery connector is out of the enclosure gate as instructed by owner.

Original v5, v6 and v7 models have been preserved; use `hardware/the_scribble_v8_rotary_fit.scad` as the active printable CAD source.

## v8.3 rounded end-slot verification (2026-10-16)

- The user's Android screenshot showed a large square opening that exposed the underlying green PCB. The actual case aperture was redesigned as a rounded, **beveled side-facing edge slot**, with a continuous upper bezel roof.
- OpenSCAD CGAL `rear`, `bezel`, and the two `side_caps` print-body STL meshes are watertight (1, 1 and 2 connected bodies respectively).
- Static **actual Elecrow STEP-derived** rotary solid, left and right key-tip meshes versus both enclosure half-meshes: **zero VTK triangle contacts** for all six tests. Additional VTK inside-case checks: 25,000 points sampled from full Elecrow assembly, all 8,455 sampled rotary vertices, each key's 1,224 vertices, plus actual battery (96), microphone (1,284), motor (4,258) each had **zero points inside either case shell**.
- Mobile HTML viewer was regenerated with those exact printable case meshes plus the original supplier-derived component meshes. A simulated Chromium/WebGL interaction test loaded 195,090 source-CAD-derived triangles, exercised touch-facing controls, and reported no JavaScript errors. This is not a live Android GPU guarantee.
- Remaining physical verification: determine whether the **3.9-mm-high capsule at Y41** is comfortable for turning/pushing the actual switch, tolerance stack-up, and inspect a first 3D print. All of these are **unverified**.
