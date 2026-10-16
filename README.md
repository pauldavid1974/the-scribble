# The Scribble

> **Enclosure status (2026-10-16):** **v8** is the active unmerged fit prototype in [PR #3](https://github.com/pauldavid1974/the-scribble/pull/3). It fixes the genuine CrowPanel **TM_2024A rotary wheel**, which v7 incorrectly replaced with a sliding piece. The board is repositioned +7 mm toward the top short edge, with a rounded, beveled end-slot that keeps the PCB covered, plus two independent pushbutton plungers. Open the **[v8 interactive source-CAD phone viewer](hardware/case_model_viewer.html)** and the [rotary CAD audit](hardware/V8_ROTARY_CLEARANCE_AUDIT.md). Static CAD clearance is promising but rotary motion, click travel, hand ergonomics and physical print remain **unverified**.

> **Distraction-Free Voice-to-Text E-Paper Handheld Recorder**

The Scribble is an open hardware, pocketable voice note capture device designed for immediate, tactile thought capture. It pairs an ultra-low-power 2.13" E-Paper display with an ESP32-S3 microcontroller, I2S digital MEMS microphone, haptic vibration engine, and rechargeable LiPo battery inside a custom 3D printed snap-fit enclosure.

Spoken thoughts are captured to internal flash memory as clean Markdown (`.md`) files and synced to a Windows PC over standard USB-C.

---


## Current v8 rotary-access prototype

The active printable source is [`hardware/the_scribble_v8_rotary_fit.scad`](hardware/the_scribble_v8_rotary_fit.scad); [`hardware/case_model_viewer.html`](hardware/case_model_viewer.html) now previews the **actual source STEP-derived rotary wheel** separately, with an **Inspect wheel** control. The 7 mm board shift, 14.2 × 3.9 mm rounded wheel-access edge slot, updated display window and true pushbutton tips are documented in [`hardware/V8_ROTARY_CLEARANCE_AUDIT.md`](hardware/V8_ROTARY_CLEARANCE_AUDIT.md). The rotary is part of the original board, **not a printed actuator**. Existing v5-v7 are archival prototypes.

### Historical v7 CAD fit trial

The archived prior mechanical source is [`hardware/the_scribble_v7_real_fit.scad`](hardware/the_scribble_v7_real_fit.scad), designed after import of the **real Elecrow board, Adafruit cell, 16×14×2.02 mm INMP441 STEP, and named 1027 motor STEP**. The adjusted outer dimensions are **46×82×20 mm**. The complete assembled STEP, generated from real component solids, is attached to the [Real CAD Source Audit Actions run](https://github.com/pauldavid1974/the-scribble/actions/runs/38950129792). See the [measured fitting report](hardware/V7_REAL_CAD_FIT_REPORT.md).

For the active **v8** source, generate actual printable prototype meshes with `node scripts/generate_stl.js --part rear` (or `bezel` / `side_caps` / `print_layout`). This tool now reads **v8** OpenSCAD directly. **The current HTML viewer includes v8.3 and isolates the actual STEP-derived rotary wheel.** The part-pair clearance evidence does not replace a full case-body CAD intersection and physical assembly test.

---

## Key Hardware Specifications

| Component | Part / Model | Dimensions / Specs | Role |
| :--- | :--- | :--- | :--- |
| **Main Board & Screen** | Elecrow CrowPanel ESP32-S3 2.13" E-Paper HMI (SKU: `DIE01021S`) | `31.20 × 63.20 × 1.60 mm` PCB, `122 × 250` resolution | Controller, 8MB PSRAM, power management, persistent note display |
| **Microphone** | INMP441 Omnidirectional I2S Digital Mic Module | `16.00 × 14.00 × 2.02 mm` breakout | Low-noise, high-fidelity voice capture via rear acoustic gasket |
| **Haptic Motor** | 1027 (10mm × 2.7mm) 3V Coin / Pancake Vibration Motor | `Ø 9.94 mm × 2.70 mm` (solder tabs `3.31 mm`) | Physical vibration confirmation on recording start/stop |
| **Haptic Driver** | Mini MOSFET Driver Breakout (SparkFun `SEN-11574` or discrete SOT-23 / TO-92) | `12.36 × 13.00 mm` | High-efficiency switching of 3V vibration motor from ESP32 GPIO |
| **Battery** | 3.7V 500mAh LiPo Cell (Size 503035) | `36.00 × 29.00 × 4.75 mm` | Multi-day standby with aggressive ESP32-S3 deep sleep |
| **Connector** | JST SH 1.0mm 2-Pin Plug & Receptacle | `BM02B-SRSS-TB` (header) & `SHR-02V-S` (housing) | Polarized, compact battery power connection |

---

## Archived Mechanical Enclosure (v5.0)

The enclosure is designed from Elecrow's official `00-2-13_view_asm.stp` CAD assembly and Eagle PCB schematics.

- **Outer Envelope:** `35.20 × 68.80 × 12.20 mm` with rounded corners (\(R = 2.60\text{ mm}\)).
- **Top Edge Overhang (0.00 mm):** The flat top casing wall spans \(X = -15.00\text{ mm} \dots +15.00\text{ mm}\) (width `30.00 mm`). The side tactile switches sit at \(X = \pm 11.15\text{ mm}\) and the center rocker wheel sits at \(X = 0.00\text{ mm}\). Because all controls are completely within the flat wall, **no buttons cut into or overhang the rounded corners**.
- **Captive Recessed Actuators:** Internal flange steps prevent buttons from falling out or binding, sitting flush with the outer wall.
- **Rear Acoustic Port:** Integrated sound channels align over the INMP441 bottom port with a `Ø 7.4 mm` OD / `Ø 5.2 mm` ID foam gasket ring.
- **Haptic C-Clip:** Integral cylindrical floor ring holds the 1027 coin motor snug against the back wall for direct vibration transfer to the user's hand.
- **Assembly:** 4-corner snap-fit pins (`Ø 3.6 mm` with `0.25 mm` socket tolerance) and bottom fingernail pry notch (`10.0 × 0.7 mm`).

---

## Repository Structure

```
the-scribble/
├── hardware/
│   ├── the_scribble_v5_step.scad   # Parametric OpenSCAD source
│   ├── the_scribble_v5_step.stl    # Print-ready 3D mesh (bottom shell, bezel, buttons)
│   ├── case_model_viewer.html      # Interactive WebGL 3D CAD inspector
│   ├── models/                     # Verified vendor STEP reference models
│   └── specs/                      # Elecrow datasheets, Eagle board, and reference STLs
├── firmware/                       # ESP32-S3 firmware (I2S, E-Paper, haptics, flash)
├── tools/
│   └── scribble_sync.py            # Windows USB-C companion sync utility
├── scripts/
│   ├── ci/project-checks.sh        # CI verification hook
│   ├── generate_stl.js             # STL generator from CAD geometry
│   └── fetch_models.py             # Automatic upstream CAD model downloader
├── AGENTS.md                       # Canonical AI & developer working agreement
├── PRD.md                          # Project brief & requirements
├── REPO_RULES.md                   # Repository governance & structure rules
└── README.md                       # This document
```

---

## 3D Printing Instructions

1. Open [`hardware/the_scribble_v5_step.stl`](file:///hardware/the_scribble_v5_step.stl) in your slicer (PrusaSlicer, Bambu Studio, OrcaSlicer, or Cura).
2. **Layer Height:** `0.16 mm` or `0.20 mm` (optimal for snap-pin spherical heads and button guide slots).
3. **Infill:** 20%–25% Gyroid or Grid.
4. **Perimeters/Walls:** 3 or 4 walls for rigid snap retention.
5. **Material:** PLA, PETG, or ABS/ASA.
6. **Supports:** No supports needed when printed flat in the provided orientation.

---


## Interactive v6 CAD Viewer (Fit Prototype)

Open [`hardware/case_model_viewer.html`](hardware/case_model_viewer.html) in Chrome or Edge. It is a single self-contained HTML file (including the preview meshes) and works offline once downloaded. It renders the **v6** rear shell, bezel, and top controls from the OpenSCAD prototype meshes, plus explicitly simplified component clearance envelopes. The viewer supports touch/mouse orbit and zoom, presets for display/rear/USB/top views, exploded assembly, component toggles, and a shell cutaway.

**Do not use the viewer's lightweight display meshes for printing.** The authoritative printable source is [`hardware/the_scribble_v6_fit.scad`](hardware/the_scribble_v6_fit.scad). Install OpenSCAD, then generate precise STL parts from that source:

```bash
node scripts/generate_stl.js --part print_layout
node scripts/generate_stl.js --part rear
node scripts/generate_stl.js --part bezel
node scripts/generate_stl.js --part side_caps
```

Generated files are saved in `output/` (or supply `--output <file>`). Review the [v6 fit audit](hardware/V6_ENCLOSURE_FIT_AUDIT.md) and [issue #2](https://github.com/pauldavid1974/the-scribble/issues/2) before test printing or installing a LiPo.
