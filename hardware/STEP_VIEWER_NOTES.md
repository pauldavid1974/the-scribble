# The Scribble v6 — Source STEP viewer notes

## What is real and what is not

- **Enclosure:** the embedded rear shell, bezel and control-cap meshes are tessellated from the v6 OpenSCAD prototype. They are not the old v5 WebGL impostor geometry. The editable SCAD source is the authoritative enclosure solid.
- **Board:** choose **Import real STEP geometry** beside the Elecrow assembly. This downloads the official upstream `00-2-13_view_asm.stp` (about 28 MB), parses it locally in your browser using OpenCascade, and replaces the PCB placeholder mesh if import succeeds. The full part orientation/position is *estimated*, NOT mechanically constrained by mating datums.
- **Battery:** on demand, import the actual Adafruit `1578` STEP included in this GitHub repository. The battery's as-shipped JST-PH connector does not match the Elecrow SH1.0 socket. The imported STEP is the *cell geometry*, not a correct wiring harness.
- **Motor:** on demand, import repository `LCM1027A2445F_1027_coin_vibration_motor.step`, an actual shape supplied with this part identifier. Orientation is estimated and real motor SKU still needs verification.
- **Microphone:** repository `denisgav__inmp441.step` is only an alternate third-party STEP and is NOT verified as the purchased 16 × 14 mm breakout. The UI labels it unverified; importing it does not certify fit.
- **Driver:** current `vibration_motor_module_snapmagic.step` is actually SparkFun `SEN-11574` (a pulse sensor), **not a valid motor driver STEP**. The driver remains a plainly labeled dimension-only placeholder. No false STEP import for it is offered.
- **Buttons, gasket and connectors:** still trial CAD/clearance features until exact purchased parts and mechanical datums are registered.

## How to use

1. Open `hardware/case_model_viewer.html` with a network connection and WebGL-capable browser (Chrome / Edge).
2. The enclosure itself appears from embedded local geometry. Component boxes are **placeholders** until they are individually imported.
3. Select **Import real STEP geometry** for the part. The parser downloads the STEP over HTTPS, uses `occt-import-js@0.0.23` (WASM) to triangulate, and shows the source shape without scaling it to fake a fit.
4. Inspect an exploded or cutaway arrangement. Hover/click source hyperlinks to verify origin. The board assembly is large and may take more memory than smaller phones provide.
5. Read the label beside each imported part. All source placements are deliberately flagged **not fit-verified**. If network/STEP parsing fails, the original placeholder remains and the viewer identifies the failure.

## Validation and limitations

- JavaScript syntax verified using Node 22 `node --check`.
- Browser interaction tested with Chromium + **mock WebGL and mock STEP importer**: the viewer became ready, displayed five STEP provenance rows (including the blocked driver), accepted a battery STEP import, updated its visible status and kept cutaway controls responsive. The mock import used a 29×36×4.75 mm sample triangulation to exercise the geometry path.
- Exact remote WASM download, Elecrow STEP parsing, the full board hierarchy transforms, physical interference, and actual GPU rendering were **not** confirmed by that test; this remains an inspection aid, not manufacturing certification.
- The parser may uniformly sample faces for display on memory-constrained devices; that approximation must never be used for engineering collision calculations. Authoritative STEP files and precise assembly registration are required for physical fit certification.
- Do not merge or label fit validated without matching actual purchased components and a physical prototype.
