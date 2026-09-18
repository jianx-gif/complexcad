import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,78))
r=w0.sketch().circle(94).circle(84,mode='s').finalize().extrude(-172).union(w0.workplane(offset=-156/2).cylinder(156,78)).union(w0.workplane(offset=16/2).cylinder(16,100))