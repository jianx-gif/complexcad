import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-35))
w1=cq.Workplane('YZ',origin=(-19,0,0))
r=w0.sketch().circle(20).circle(15,mode='s').finalize().extrude(70).union(w1.workplane(offset=47/2).moveTo(0,-1).cylinder(47,3))
