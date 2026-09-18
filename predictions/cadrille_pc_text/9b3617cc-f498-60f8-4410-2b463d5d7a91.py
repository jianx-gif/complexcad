import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-92))
r=w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(44).union(w0.workplane(offset=158/2).moveTo(0,-2).cylinder(158,61)).union(w0.sketch().circle(37).circle(10,mode='s').finalize().extrude(184))