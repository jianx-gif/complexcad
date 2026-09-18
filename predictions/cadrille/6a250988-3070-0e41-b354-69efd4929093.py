import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,63))
w1=cq.Workplane('YZ',origin=(85,0,0))
r=w0.sketch().circle(100).circle(40,mode='s').finalize().extrude(-143).union(w1.workplane(offset=-147/2).moveTo(0,18).cylinder(147,55))