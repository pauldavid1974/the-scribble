#!/usr/bin/env python3
"""Source-STEP static switch clearance against OpenSCAD v8 case meshes.

No hand-drawn rotary-wheel envelope is permitted. Exact Elecrow STEP solids
are triangulated and checked for triangle contacts against exported v8 shell.
Mechanical travel and ergonomics are NOT established by this test.
"""
from pathlib import Path
import tempfile

import trimesh
import vtk
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Trsf
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.StlAPI import StlAPI_Writer
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SHELLS={p:trimesh.load(ROOT/f"output/the_scribble_v8_{p}.stl",force="mesh") for p in ("rear","bezel")}
CAPS=trimesh.load(ROOT/"output/the_scribble_v8_side_caps.stl",force="mesh").split()
assert len(CAPS)==2,"v8 has only MENU and EXIT plungers, no fake rotary actuator"
for cap in CAPS:cap.apply_translation([0,36,12.56])

def bounds(s):
    box=Bnd_Box()
    box.SetGap(0)
    BRepBndLib.Add_s(s,box,False)
    x0,y0,z0,x1,y1,z1=box.Get()
    return np.array([[x0,y0,z0],[x1,y1,z1]])

def poly(mesh):
    pts=vtk.vtkPoints()
    pts.SetData(numpy_to_vtk(mesh.vertices.astype("float64"),deep=True))
    cells=vtk.vtkCellArray()
    arr=np.column_stack((np.full(len(mesh.faces),3),mesh.faces)).ravel().astype("int64")
    cells.SetCells(len(mesh.faces),numpy_to_vtkIdTypeArray(arr,deep=True))
    result=vtk.vtkPolyData()
    result.SetPoints(pts)
    result.SetPolys(cells)
    return result

def contacts(a,b):
    filt=vtk.vtkCollisionDetectionFilter()
    filt.SetInputData(0,poly(a))
    filt.SetInputData(1,poly(b))
    tr=vtk.vtkTransform()
    filt.SetTransform(0,tr)
    filt.SetTransform(1,tr)
    filt.SetCollisionModeToFirstContact()
    filt.SetNumberOfCellsPerNode(6)
    filt.SetBoxTolerance(0.0001)
    filt.SetCellTolerance(0)
    filt.Update()
    return filt.GetNumberOfContacts()

board=ROOT/"hardware/specs/00-2-13_view_asm.stp"
reader=STEPControl_Reader()
assert reader.ReadFile(str(board))==IFSelect_RetDone, "missing official CrowPanel STEP"
assert reader.TransferRoots()
walk=TopExp_Explorer(reader.OneShape(),TopAbs_SOLID)
sources={}
i=0
while walk.More():
    if i in (2,5,8):sources[i]=walk.Current()
    i+=1
    walk.Next()
assert i>=240 and set(sources)=={2,5,8},"unexpected official STEP component list"

# Same as hardware/assemble_real_step.py: whole board moved +7 in case Y.
transform=gp_Trsf()
transform.SetValues(1,0,0,0, 0,0,-1,5.63785, 0,1,0,16.952)
expected={
  2:np.array([[-6.582,30.988,13.152],[6.582,39.981,15.952]]),
  5:np.array([[-12.650,36.538,12.860],[-9.650,38.038,14.360]]),
  8:np.array([[9.650,36.538,12.860],[12.650,38.038,14.360]])
}
with tempfile.TemporaryDirectory() as d:
    for idx,nm in ((2,"rotary"),(5,"left_key"),(8,"right_key")):
        shape=BRepBuilderAPI_Transform(sources[idx],transform,True).Shape()
        bb=bounds(shape)
        assert np.allclose(bb,expected[idx],atol=.015),f"{nm} is not at expected actual-CAD location: {bb}"
        BRepMesh_IncrementalMesh(shape,.08,False,.2)
        path=Path(d)/f"{nm}.stl"
        assert StlAPI_Writer().Write(shape,str(path))
        model=trimesh.load(str(path),force="mesh")
        for part,shell in SHELLS.items():
            n=contacts(model,shell)
            print(f"REAL_SWITCH_COLLISION {nm} {part} contact_triangles={n}",flush=True)
            assert n==0, f"{nm} hits {part}"
        if idx in (5,8):
            cap=CAPS[0 if idx==5 else 1]
            n=contacts(model,cap)
            print(f"REAL_KEY_TO_PLUNGER {nm} contact_triangles={n}",flush=True)
            assert n==0, f"{nm} conflicts with cap at rest"
    for ci,cap in enumerate(CAPS):
        for part,shell in SHELLS.items():
            n=contacts(cap,shell)
            print(f"BUTTON_TO_CASE cap={ci} {part} contact_triangles={n}",flush=True)
            assert n==0
print("PASS: v8 static switch/rotary geometry clear using actual Elecrow STEP",flush=True)
print("NOT TESTED: switch rotation/click stroke, physical FDM tolerances or finger ergonomics")
