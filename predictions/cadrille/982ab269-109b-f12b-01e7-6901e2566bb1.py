import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,53))
r=w0.sketch().circle(68).circle(64,mode='s').finalize().extrude(-132).union(w0.workplane(offset=-128/2).cylinder(128,64)).union(w0.workplane(offset=21/2).cylinder(21,100))