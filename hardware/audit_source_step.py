#!/usr/bin/env python3
"""Exact vendor STEP ingestion. No surrogate solids, automatic scaling or guessed fit claims.

This first stage reports the B-rep bounds of every supplied model. It deliberately
does NOT certify assembly interference until board-local placements are registered.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import urllib.request

from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "hardware/specs/00-2-13_view_asm.stp"
BOARD_URL = ("https://raw.githubusercontent.com/Elecrow-RD/"
             "CrowPanel-ESP32-2.13-E-paper-HMI-Display-with-122-250/"
             "master/3D%20file/00-2-13_view_asm.stp")

def download_board():
    BOARD.parent.mkdir(parents=True, exist_ok=True)
    if BOARD.exists() and BOARD.stat().st_size > 1_000_000:
        return
    request = urllib.request.Request(BOARD_URL, headers={"User-Agent": "ScribbleMechanicalAudit/1.0"})
    with urllib.request.urlopen(request, timeout=120) as reply, BOARD.open("wb") as dest:
        while block := reply.read(1024 * 1024):
            dest.write(block)

def measure_step(path: Path):
    raw = path.read_bytes()
    header = raw[:512].decode("ascii", errors="replace")
    result = dict(name=path.name, bytes=len(raw), header=header[:140])
    try:
        reader = STEPControl_Reader()
        status = reader.ReadFile(str(path))
        if status != IFSelect_RetDone:
            result.update(valid=False, error=f"OpenCascade ReadFile status {int(status)}")
            return result
        roots = reader.TransferRoots()
        shape = reader.OneShape()
        box = Bnd_Box()
        box.SetGap(0.0)
        BRepBndLib.Add_s(shape, box, False)
        if box.IsVoid():
            result.update(valid=False, error="STEP transferred with no bounded geometry")
            return result
        x0,y0,z0,x1,y1,z1 = box.Get()
        bounds = [[round(a, 4), round(b, 4)] for a,b in zip([x0,y0,z0],[x1,y1,z1])]
        dimensions = [round(b-a,4) for a,b in zip([x0,y0,z0],[x1,y1,z1])]
        ex = TopExp_Explorer(shape,TopAbs_SOLID)
        solids=0
        while ex.More():
            solids+=1
            ex.Next()
        result.update(valid=True, dimensions_mm=dimensions, bounds_mm=bounds,
                      transferred_roots=roots, solids=solids)
    except Exception as exc:
        result.update(valid=False,error=f"{type(exc).__name__}: {exc}")
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--skip-board-download",action="store_true")
    parser.add_argument("--output",default="output/cad-source-audit.json")
    args=parser.parse_args()
    errors=[]
    if not args.skip_board_download:
        try: download_board()
        except Exception as exc: errors.append(f"Official Elecrow STEP fetch: {type(exc).__name__}: {exc}")
    paths=[BOARD] + sorted((ROOT/"hardware/models").glob("*.step")) + sorted((ROOT/"hardware/models").glob("*.stp"))
    data=[measure_step(p) for p in paths if p.exists()]
    for i in data:
        print(f'{"REAL STEP" if i["valid"] else "FAILED STEP"} {i["name"]}: '
              f'{i.get("dimensions_mm", i.get("error"))}, solids={i.get("solids","?")}',flush=True)
    def pick(fragment):
        return next((d for d in data if fragment.lower() in d["name"].lower()),None)
    batt=pick("adafruit_1578")
    checks={
      "board_vendor_step_imported": bool(pick("00-2-13") and pick("00-2-13")["valid"]),
      "battery_step_imported":bool(batt and batt["valid"]),
      "motor_step_imported":bool(pick("LCM1027A2445F") and pick("LCM1027A2445F")["valid"]),
      "inmp441_alternative_imported":any(d["valid"] and "inmp441" in d["name"].lower() for d in data),
      "driver_complete_module_verified":False,
      "board_brep_registered_to_eagle_datums":False,
      "full_assembly_interference_test_passed":False,
    }
    if batt and batt.get("valid"):
        checks["battery_step_expected_envelope"] = all(
          abs(a-b) < 0.6 for a,b in zip(sorted(batt["dimensions_mm"]),[4.75,29,36]))
    report={
      "disposition":"NOT VERIFIED — actual STEP import does not establish placement or interference",
      "check_type":"native OpenCascade STEP B-rep (not viewer boxes)",
      "source_models":data,"checks":checks,"errors":errors,
      "selection":"README names generic INMP441 and alternative drivers; exact as-purchased model not defined",
      "battery_connector":"Excluded from mechanical clearance gate at owner direction",
    }
    output=ROOT/args.output
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+"\n")
    print("CHECKS",json.dumps(checks,sort_keys=True),flush=True)
    print(f"REPORT={output}",flush=True)
    # Model ingestion failures must be transparent; fail only if central sources unavailable.
    if not checks["board_vendor_step_imported"]:
       raise SystemExit("BLOCKED: exact main-board STEP could not be imported")
    if not checks["battery_step_imported"]:
       raise SystemExit("BLOCKED: listed battery STEP could not be imported")

if __name__=="__main__":main()
