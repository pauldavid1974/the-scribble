#!/usr/bin/env python3
"""Assemble actual part STEP B-reps for mechanical fit checking.

No primitive substitutes and no silent rescaling. This is an ENGINEERING TRIAL
with explicit datum assumptions; unverified orientation is not a certified fit.
"""
from __future__ import annotations
import json
from pathlib import Path
from itertools import combinations

from OCP.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.gp import gp_Trsf
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/"hardware/models"
COMPONENTS={
 "crowpanel": ROOT/"hardware/specs/00-2-13_view_asm.stp",
 "battery": MODEL/"adafruit_1578_500mAh_battery.step",
 "microphone":MODEL/"paulrenzi__bought_inmp441.step",
 "motor":MODEL/"LCM1027A2445F_1027_coin_vibration_motor.step",
 "driver_sot23":MODEL/"SOT-23.step",
 "driver_diode":MODEL/"D_SOD-323.step",
}

# Rigid 3D rotations only; approved measured bounding extents of actual STEP.
# These are a proposed assembly pose, NOT coordinate mating constraints.
# CrowPanel maker STEP: X width, Z length, Y height, front toward +Y.
# Align center to Eagle PCB centroid and put lower-most electronics at z=1.9.
TRANSFORMS={
 "crowpanel":[1,0,0, 0,
              0,0,-1,-1.36215,
              0,1,0,16.952],
 # Adafruit cell actual axes: 36 along X, 29 along Y; rotate 90 degrees.
 "battery":[0,1,0,-14.5,
            -1,0,0,15.5,
            0,0,1,1.85],
 # Actual 16 x 14 x 2.02mm third-party mic: thickness axis source Y.
 "microphone":[1,0,0,-543.8,
               0,0,1,17.5,
               0,-1,0,-11.75],
 # Actual LCM motor STEP contains tabs/wires projecting along STEP -Z.
 # Aim those features inboard to +Y, away from lower snap tower.
 "motor":[1,0,0,-7,
          0,0,-1,-31.5,
          0,1,0,3.7278],
 # These SOT-23/diode models are actual discrete package STEP solids,
 # NOT a selected assembled circuit board/module. Never certify the driver.
 "driver_sot23":[1,0,0,8.0,
                 0,1,0,-31.8,
                 0,0,1,2.05],
 "driver_diode":[1,0,0,13.0,
                 0,1,0,-31.8,
                 0,0,1,2.05],
}

def load(path):
    if not path.exists():raise FileNotFoundError(path)
    reader=STEPControl_Reader()
    if reader.ReadFile(str(path))!=IFSelect_RetDone:
        raise ValueError(f"invalid STEP: {path}")
    if not reader.TransferRoots():
        raise ValueError(f"zero STEP roots: {path}")
    return reader.OneShape()

def relocate(shape,name):
    t=gp_Trsf()
    t.SetValues(*TRANSFORMS[name])
    assert abs(t.ScaleFactor()-1)<1e-6,(name,t.ScaleFactor())
    return BRepBuilderAPI_Transform(shape,t,True).Shape()

def bounds(shape):
    box=Bnd_Box()
    box.SetGap(0)
    BRepBndLib.Add_s(shape,box,False)
    x0,y0,z0,x1,y1,z1=box.Get()
    return [[round(lo,4),round(hi,4)] for lo,hi in zip([x0,y0,z0],[x1,y1,z1])]

def bounding_overlap(a,b):
    bounds_a,bounds_b=bounds(a),bounds(b)
    return all(min(aa[1],bb[1])-max(aa[0],bb[0]) > 0.001 for aa,bb in zip(bounds_a,bounds_b))

def solids(shape):
    explorer=TopExp_Explorer(shape,TopAbs_SOLID)
    found=False
    while explorer.More():
        found=True
        yield explorer.Current()
        explorer.Next()
    if not found:
        yield shape

def exact_intersection_volume(a,b):
    # Narrow-phase BRep Booleans on real individual vendor solids. Performing
    # an entire 240-body CrowPanel vs. cell in one operation can stall OCC.
    left=list(solids(a))
    right=list(solids(b))
    amount=0.0
    tested=0
    for one in left:
        for two in right:
            if not bounding_overlap(one,two):
                continue
            tested+=1
            operation=BRepAlgoAPI_Common(one,two)
            operation.SetRunParallel(False)
            operation.Build()
            if not operation.IsDone():
                raise RuntimeError("OpenCascade BRep Common failed")
            props=GProp_GProps()
            BRepGProp.VolumeProperties_s(operation.Shape(),props)
            amount+=abs(props.Mass())
    print("NARROW_PHASE",len(left),len(right),"candidate_pairs",tested,flush=True)
    return round(amount,5)

def main():
    out=ROOT/"output"
    out.mkdir(exist_ok=True)
    shapes={}
    poses=[]
    for name,path in COMPONENTS.items():
        native=load(path)
        placed=relocate(native,name)
        shapes[name]=placed
        info={"name":name,"source":str(path.relative_to(ROOT)),"bounds_mm":bounds(placed),
              "pose_is_verified":False}
        poses.append(info)
        print("ACTUAL SOLID",name,info["bounds_mm"],flush=True)

    checks=[]
    for a,b in combinations(shapes,2):
        # Only run expensive exact Booleans for pairs whose AABBs intersect.
        # Board STEP is a multi-body assembly; OpenCascade may report native
        # CAD overlaps for nested transparent parts, so include evidence.
        if not bounding_overlap(shapes[a],shapes[b]):
            checks.append(dict(a=a,b=b,overlap_mm3=0,method="disjoint AABB proof"))
            continue
        try:
            volume=exact_intersection_volume(shapes[a],shapes[b])
            checks.append(dict(a=a,b=b,overlap_mm3=volume,
                               method="native OpenCascade B-rep Boolean"))
            print("INTERFERENCE",a,b,volume,"mm3",flush=True)
        except Exception as e:
            checks.append(dict(a=a,b=b,overlap_mm3=None,
                               error=f"{type(e).__name__}: {e}"))
            print("INTERFERENCE UNKNOWN",a,b,e,flush=True)

    compound=TopoDS_Compound()
    builder=BRep_Builder()
    builder.MakeCompound(compound)
    for shape in shapes.values():builder.Add(compound,shape)
    writer=STEPControl_Writer()
    writer.Transfer(compound,STEPControl_AsIs)
    dest=out/"the_scribble_actual_component_assembly.step"
    if writer.Write(str(dest))!=IFSelect_RetDone:
        raise SystemExit("FAILED to save STEP assembly")
    report={
      "status":"V7 INTERNAL SOURCE-CAD TRIAL — DATUM AND CASE CLEARANCES NEED VERIFICATION",
      "source":"real imported vendor STEP B-reps; no scaled proxy geometry",
      "models":poses,"pairwise_intersections":checks,
      "board_registration":"rotation/translation hypothesized from Elecrow STEP bounds and Eagle locations, not validated by registration of specific CAD landmarks",
      "motor":"LCM1027A2445F includes tabs/wires; full imported geometry, not nominal 10mm cylinder",
      "microphone":"paulrenzi STEP exact nominal 16 x 14 x 2.02mm match; unconfirmed vendor SKU",
      "driver":"real SOT23 and SOD323 package STEP only, not verified complete driver PCB",
      "battery_connector":"ignored for enclosure packaging by owner instruction",
      "enclosure_collision":"NOT YET VERIFIED — native component pair tests do not prove collision-free CSG case",
      "file":dest.name,
    }
    (out/"real_assembly_report.json").write_text(json.dumps(report,indent=2)+"\n")
    print("ASSEMBLY_STEP",dest,"SIZE_BYTES",dest.stat().st_size,flush=True)
    print("ASSEMBLY_REPORT",json.dumps({k:v for k,v in report.items() if k in ("status","pairwise_intersections","enclosure_collision")}),flush=True)

if __name__=="__main__":main()
