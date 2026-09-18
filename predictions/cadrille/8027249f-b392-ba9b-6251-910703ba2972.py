import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-1))
r=w0.workplane(offset=-11/2).moveTo(0,-13).box(174,66,11).union(w0.workplane(offset=13/2).box(14,200,13))