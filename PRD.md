# Project brief / PRD — The Scribble

> **What this is:** The canonical project-level brief for **The Scribble** — a dedicated, distraction-free handheld voice-to-text capture and note-taking device built on the Elecrow CrowPanel ESP32-S3 2.13" E-Paper display.

## Problem / why
Audio note capture often relies on smartphones or complex recorders that introduce distractions, short battery lives, high latency, or forced cloud lock-in. The Scribble provides a tactile, dedicated, pocketable hardware device designed for instant one-button thought capture with persistent, readable E-Paper display and private, local USB-C sync.

## Goal / outcome
Design, assemble, and deliver the production-ready 3D printable mechanical enclosure, ESP32-S3 firmware, and Windows companion USB-C sync tool for **The Scribble**.

## Users / context
- **Primary User:** Paul David.
- **Context:** Everyday pocket carry, desk-side quick memos, and walking/on-the-go thought capture. Notes sync to a local Windows 11 PC via USB-C serial.

## Scope
- **In:**
  - **Enclosure & Packaging:** Custom two-piece snap-fit 3D printable case (`35.20 × 68.80 × 12.20 mm`, R=2.6mm corners) with 0.00 mm button overhang on the top edge, flush captive actuators, rear acoustic port with gasket seal, vibration motor C-clip ring, battery cradle, and right-edge USB-C cutout.
  - **Hardware Subsystems:**
    - Elecrow CrowPanel ESP32-S3 2.13" E-Paper HMI (`122 × 250` resolution, 8MB PSRAM).
    - INMP441 I2S omnidirectional digital MEMS microphone breakout.
    - 1027 (10mm × 2.7mm) 3V coin vibration motor with mini MOSFET driver for haptic feedback.
    - 3.7V 500mAh LiPo battery (503035 form factor: `36.0 × 29.0 × 4.75 mm`) with JST SH 1.0mm 2-pin connector.
  - **Firmware (ESP32-S3):**
    - Audio recording via I2S DMA.
    - Voice transcription / Markdown note generation saved directly to internal flash as `.md` files.
    - 2.13" E-Paper partial and full refresh rendering for note text, battery state, and recording status.
    - Distinct haptic feedback patterns (start record, stop record, note saved, low battery).
    - Deep sleep power management with wake-on-interrupt from top tactile switches.
  - **Desktop Companion Sync:**
    - Windows CLI / script to detect connected device over USB-C, read/pull `.md` notes, manage storage, and set device time.
  - **CAD / 3D Assets:**
    - Parametric OpenSCAD source (`the_scribble_v5_step.scad`), print-ready STL (`the_scribble_v5_step.stl`), and interactive WebGL inspection viewer (`case_model_viewer.html`).
- **Out (for now):**
  - Storing raw uncompressed `.wav` audio files (dropped to conserve flash storage and focus on immediate `.md` text notes).
  - Speaker / audio playback hardware (all user feedback is provided via haptic vibration pulses and the E-Paper display).
  - Mandatory cloud connectivity or third-party proprietary mobile apps (100% private and offline-capable).

## Requirements
- **Audio Capture:** One-touch recording via captive top-edge button; captures high-clarity voice through rear sound port gasket.
- **Physical Interface:** Flush top edge with 0.00 mm button overhang. Rocker wheel for scrolling through previous notes. Exit/Back and Menu buttons.
- **Low-Power Display:** E-Paper maintains note view with zero power draw when sleeping.
- **Haptic Feedback:** Instant vibration pulse confirms recording start/stop without looking at the screen.
- **USB-C Synchronization:** Plugs into Windows PC to charge and sync notes as clean Markdown.

## Non-functional needs
- **Security / Privacy:** 100% local, offline device. No telemetry, no cloud dependence.
- **Battery Life:** Multiple days to weeks of standby with multiple recordings per day on 500mAh LiPo cell via aggressive deep sleep.
- **Form Factor:** Compact, rounded, pocketable design with robust snap-fit retention and tool-free disassembly pry slot.

## Constraints / decisions already made
- **Controller & Display:** Elecrow CrowPanel 2.13" E-Paper Display (SKU: DIE01021S / ESP32-S3 8MB PSRAM).
- **Physical Controls:** Top-edge `KEY-579` tactile push buttons and `XB-TM-2024A` 3-way thumb rocker wheel.
- **Mounting & Tolerances:** Snap pins `Ø 3.6 mm` with `0.25 mm` socket tolerance. Component clearance `0.20 mm` perimeter.
- **Battery & Power:** 503035 500mAh LiPo cell with JST SH 1.0mm vertical SMD header (`BM02B-SRSS-TB`) and female plug housing (`SHR-02V-S`).

## Success criteria
1. 3D printed enclosure snaps together cleanly with no component binding or button sticking, maintaining flush 0.00 mm top overhang.
2. Holding the Talk button vibrates the motor and records voice input.
3. Spoken thoughts are transcribed to `.md` format and displayed on the 2.13" E-Paper screen.
4. Connecting to PC via USB-C mounts or syncs all Markdown files to the user's notes folder.

## Milestones
1. **Milestone 1 — CAD & Physical Assembly:** Enclosure 3D print verification, component fit check, snap-fit test, and button travel validation.
2. **Milestone 2 — Firmware Core:** Audio capture via INMP441, E-Paper display driver integration, and haptic motor signaling.
3. **Milestone 3 — Note Storage & Sync:** Flash filesystem storage for `.md` notes, USB serial protocol, and Windows sync CLI.
