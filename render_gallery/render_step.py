# -*- coding: utf-8 -*-
"""Render CAD models from their exact B-rep (STEP) instead of an STL mesh.

Faces are tessellated finely from the B-rep and shaded with the surface's own normals (smooth on curved
faces, crisp at sharp edges); on top, only the true B-rep edges are drawn (seam and degenerate edges
skipped), with depth testing, so no triangle of the tessellation is visible. Offscreen VTK rendering.

    shape_from(path)  -> TopoDS_Shape from .step/.stp, or by executing a CadQuery .py (subprocess, STEP export)
    render(path, color, size=900) -> HxWx3 uint8 image, or None if the program does not execute
Input meshes (.stl) that have no B-rep are rendered with the same shading, smooth normals and feature edges.
"""
import os, sys, subprocess, hashlib
import numpy as np
import vtk
from vtkmodules.util.numpy_support import vtk_to_numpy
import cadquery as cq
from OCP.TopExp import TopExp, TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape, TopTools_IndexedMapOfShape
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

HERE = os.path.dirname(os.path.abspath(__file__))
SATURATION = 0.32          # share of the colour's saturation kept (muted palette)
TMP = os.path.join(HERE, '_figtmp', 'step')
os.makedirs(TMP, exist_ok=True)
PY = sys.executable
EXEC = os.path.join(HERE, 'exec_to_step.py')


def shape_from(path, timeout=150):
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.step', '.stp'):
        return cq.importers.importStep(path).val().wrapped
    if ext == '.py':
        key = hashlib.md5(os.path.abspath(path).encode()).hexdigest()[:12]
        out = os.path.join(TMP, os.path.basename(path)[:-3] + '_' + key + '.step')
        if not os.path.isfile(out):
            try:
                r = subprocess.run([PY, '-X', 'utf8', EXEC, path, out], capture_output=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                return None
            if r.returncode != 0 or not os.path.isfile(out):
                return None
        return cq.importers.importStep(out).val().wrapped
    raise ValueError('not a B-rep source: ' + path)


def _bbox(shape):
    b = Bnd_Box(); BRepBndLib.Add_s(shape, b)
    x0, y0, z0, x1, y1, z1 = b.Get()
    return np.array([x0, y0, z0]), np.array([x1, y1, z1])


def _surface_polydata(shape, diag):
    pd = cq.Shape(shape).toVtkPolyData(tolerance=diag * 4e-4, angularTolerance=0.08, normals=False)
    only = vtk.vtkPolyData(); only.SetPoints(pd.GetPoints()); only.SetPolys(pd.GetPolys())
    clean = vtk.vtkCleanPolyData(); clean.SetInputData(only); clean.Update()
    nf = vtk.vtkPolyDataNormals(); nf.SetInputConnection(clean.GetOutputPort())
    nf.SetFeatureAngle(35.0); nf.SplittingOn(); nf.ConsistencyOn(); nf.AutoOrientNormalsOff()
    nf.ComputePointNormalsOn(); nf.Update()
    return nf.GetOutput()


def _edge_polydata(shape, diag):
    """true B-rep edges, each once; seam edges (closed on one face) and degenerate edges skipped"""
    emap = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(shape, TopAbs_EDGE, TopAbs_FACE, emap)
    pts = vtk.vtkPoints(); lines = vtk.vtkCellArray(); defl = diag * 3e-4
    for i in range(1, emap.Extent() + 1):
        e = TopoDS.Edge_s(emap.FindKey(i))
        if BRep_Tool.Degenerated_s(e):
            continue
        faces = emap.FindFromIndex(i)
        seam = False
        it = faces.cbegin() if hasattr(faces, 'cbegin') else None
        for f in faces:
            if BRep_Tool.IsClosed_s(e, TopoDS.Face_s(f)):
                seam = True; break
        if seam:
            continue
        try:
            c = BRepAdaptor_Curve(e); d = GCPnts_QuasiUniformDeflection(c, defl)
            if not d.IsDone() or d.NbPoints() < 2:
                continue
            ids = []
            for k in range(1, d.NbPoints() + 1):
                p = c.Value(d.Parameter(k)); ids.append(pts.InsertNextPoint(p.X(), p.Y(), p.Z()))
            pl = vtk.vtkPolyLine(); pl.GetPointIds().SetNumberOfIds(len(ids))
            for k, pid in enumerate(ids):
                pl.GetPointIds().SetId(k, pid)
            lines.InsertNextCell(pl)
        except Exception:
            continue
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetLines(lines)
    return pd


def _mesh_polydata(stl):
    r = vtk.vtkSTLReader(); r.SetFileName(stl); r.Update()
    clean = vtk.vtkCleanPolyData(); clean.SetInputConnection(r.GetOutputPort()); clean.Update()
    nf = vtk.vtkPolyDataNormals(); nf.SetInputConnection(clean.GetOutputPort())
    nf.SetFeatureAngle(35.0); nf.SplittingOn(); nf.ConsistencyOn(); nf.Update()
    fe = vtk.vtkFeatureEdges(); fe.SetInputConnection(clean.GetOutputPort())
    fe.BoundaryEdgesOn(); fe.FeatureEdgesOn(); fe.SetFeatureAngle(35.0); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff()
    fe.ColoringOff(); fe.Update()
    b = np.array(clean.GetOutput().GetBounds()).reshape(3, 2)
    return nf.GetOutput(), fe.GetOutput(), b[:, 0], b[:, 1]


def _hex(c):
    c = c.lstrip('#'); return np.array([int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4)])


def render(path, color, size=900, elev=22.0, azim=-60.0, edge_width=1.6):
    """returns an RGB uint8 image of the model, or None if it cannot be built."""
    if path.lower().endswith('.stl'):
        surf, edges, lo, hi = _mesh_polydata(path)
    else:
        shape = shape_from(path)
        if shape is None:
            return None
        lo, hi = _bbox(shape)
        diag = float(np.linalg.norm(hi - lo)) or 1.0
        surf = _surface_polydata(shape, diag); edges = _edge_polydata(shape, diag)
    import colorsys
    h, l, sat = colorsys.rgb_to_hls(*_hex(color))
    base = np.array(colorsys.hls_to_rgb(h, min(0.70, l + 0.16), sat * SATURATION))   # muted, low-saturation fill
    ren = vtk.vtkRenderer(); ren.SetBackground(1, 1, 1)
    sm = vtk.vtkPolyDataMapper(); sm.SetInputData(surf); sm.ScalarVisibilityOff()
    sm.SetResolveCoincidentTopologyToPolygonOffset()
    sm.SetRelativeCoincidentTopologyPolygonOffsetParameters(1.2, 1.2)
    sa = vtk.vtkActor(); sa.SetMapper(sm)
    pr = sa.GetProperty(); pr.SetColor(*base); pr.SetInterpolationToPhong()
    pr.SetAmbient(0.26); pr.SetDiffuse(0.70); pr.SetSpecular(0.10); pr.SetSpecularPower(28)
    ren.AddActor(sa)
    em = vtk.vtkPolyDataMapper(); em.SetInputData(edges); em.ScalarVisibilityOff()
    ea = vtk.vtkActor(); ea.SetMapper(em)
    ep = ea.GetProperty(); ep.SetColor(0.22, 0.23, 0.25); ep.SetLineWidth(edge_width); ep.SetLighting(False)
    ren.AddActor(ea)
    lk = vtk.vtkLightKit(); lk.SetKeyLightIntensity(0.95); lk.AddLightsToRenderer(ren)
    c = (lo + hi) / 2.0; r = float(np.linalg.norm(hi - lo)) / 2.0 or 1.0
    el, az = np.radians(elev), np.radians(azim)
    d = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    cam = ren.GetActiveCamera(); cam.ParallelProjectionOn()
    cam.SetFocalPoint(*c); cam.SetPosition(*(c + d * r * 6)); cam.SetViewUp(0, 0, 1)
    ren.ResetCamera(); cam.SetParallelScale(r * 1.02)
    win = vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetMultiSamples(8)
    win.SetSize(size, size); win.AddRenderer(ren); win.Render()
    w2i = vtk.vtkWindowToImageFilter(); w2i.SetInput(win); w2i.SetInputBufferTypeToRGB(); w2i.ReadFrontBufferOff(); w2i.Update()
    img = w2i.GetOutput(); dims = img.GetDimensions()
    arr = vtk_to_numpy(img.GetPointData().GetScalars()).reshape(dims[1], dims[0], 3)[::-1]
    win.Finalize()
    return arr.copy()


def crop(img, pad=12):
    """trim white margins, keep a small pad, return a square canvas"""
    m = (img < 250).any(axis=2)
    if not m.any():
        return img
    ys, xs = np.where(m)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + pad, img.shape[0]), max(xs.min() - pad, 0), min(xs.max() + pad, img.shape[1])
    sub = img[y0:y1, x0:x1]; h, w = sub.shape[:2]; s = max(h, w)
    out = np.full((s, s, 3), 255, np.uint8); out[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = sub
    return out
