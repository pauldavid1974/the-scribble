#!/usr/bin/env python3
"""
scripts/fetch_models.py — Download official / vendor CAD models for The Scribble.
Downloads upstream STEP models and reference CAD assemblies on demand.
"""

import os
import sys
import urllib.request
import urllib.parse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARDWARE_DIR = os.path.join(REPO_ROOT, "hardware")
MODELS_DIR = os.path.join(HARDWARE_DIR, "models")
SPECS_DIR = os.path.join(HARDWARE_DIR, "specs")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(SPECS_DIR, exist_ok=True)

UPSTREAM_MODELS = [
    # (Destination path relative to repo, URL, Description)
    (
        os.path.join(SPECS_DIR, "00-2-13_view_asm.stp"),
        "https://raw.githubusercontent.com/Elecrow-RD/CrowPanel-ESP32-2.13-E-paper-HMI-Display-with-122-250/master/3D%20file/00-2-13_view_asm.stp",
        "Elecrow CrowPanel 2.13 E-Paper Official STEP Assembly (28.3 MB)"
    ),
    (
        os.path.join(MODELS_DIR, "adafruit_1578_500mAh_battery.step"),
        "https://raw.githubusercontent.com/adafruit/Adafruit_CAD_Parts/main/1578%20500mAh%20battery/1578%20500mAh%20battery.step",
        "Adafruit 500mAh LiPo Battery (503035 form factor)"
    ),
    (
        os.path.join(MODELS_DIR, "paulrenzi__bought_inmp441.step"),
        "https://raw.githubusercontent.com/paulrenzi/bought/HEAD/bought_components/microphone/inmp441.step",
        "INMP441 I2S Digital Microphone Breakout Board"
    ),
    (
        os.path.join(MODELS_DIR, "JST_SHR-02V-S_female_plug.step"),
        "https://raw.githubusercontent.com/zynthian/zynthian-hw/HEAD/Zynaptik_v3/lib/3D/jst-sh-smd-connectors-1.snapshot.4/SHR-xxV-S/SHR-02V-S.STEP",
        "JST SH 1.0mm 2-pin Female Crimp Plug Housing (SHR-02V-S)"
    ),
    (
        os.path.join(MODELS_DIR, "JST_SHR-02V-S-B_female_plug.step"),
        "https://raw.githubusercontent.com/zynthian/zynthian-hw/HEAD/Zynaptik_v3/lib/3D/jst-sh-smd-connectors-1.snapshot.4/SHR-xxV-S-B/SHR-02V-S-B.STEP",
        "JST SH 1.0mm 2-pin Female Crimp Plug Housing with Locking Boss (SHR-02V-S-B)"
    ),
    (
        os.path.join(MODELS_DIR, "JST_SH_BM02B-SRSS-TB_1x02-1MP_P1.00mm_Vertical.step"),
        "https://gitlab.com/kicad/libraries/kicad-packages3D/-/raw/master/Connector_JST.3dshapes/JST_SH_BM02B-SRSS-TB_1x02-1MP_P1.00mm_Vertical.step",
        "JST SH BM02B-SRSS-TB 1.0mm 2-Pin Vertical SMD Board Header"
    )
]

def fetch_file(dst, url, desc):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        print(f"  [EXISTS] {os.path.basename(dst)} ({os.path.getsize(dst):,} bytes) — {desc}")
        return True
    print(f"  [FETCHING] {os.path.basename(dst)}: {desc}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(dst, "wb") as f:
            f.write(r.read())
        print(f"  [DONE] Saved {os.path.basename(dst)} ({os.path.getsize(dst):,} bytes)")
        return True
    except Exception as e:
        print(f"  [FAIL] Could not fetch {url}: {e}")
        return False

def main():
    print("==> Checking / Fetching Upstream 3D CAD Models for The Scribble...")
    success = 0
    for dst, url, desc in UPSTREAM_MODELS:
        if fetch_file(dst, url, desc):
            success += 1
    print(f"==> Processed {len(UPSTREAM_MODELS)} models ({success} available).")

if __name__ == "__main__":
    main()
