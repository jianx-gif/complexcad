import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,68))
w1=cq.Workplane('YZ',origin=(85,0,0))
r=w0.sketch().circle(100).circle(40,mode='s').finalize().extrude(-148).union(w1.workplane(offset=-167/2).moveTo(0,5).cylinder(167,68))