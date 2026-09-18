import cadquery as cq
w0=cq.Workplane('YZ',origin=(-10,0,0))
w1=cq.Workplane('XY',origin=(0,0,-99))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(29).union(w1.sketch().circle(99).circle(27,mode='s').finalize().extrude(199))