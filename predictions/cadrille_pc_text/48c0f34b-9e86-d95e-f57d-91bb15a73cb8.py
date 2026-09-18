import cadquery as cq
w0=cq.Workplane('YZ',origin=(-27,0,0))
w1=cq.Workplane('XY',origin=(0,0,19))
r=w0.sketch().circle(41).circle(27,mode='s').finalize().extrude(49).union(w0.sketch().circle(37).circle(26,mode='s').finalize().extrude(112)).union(w1.sketch().circle(100).circle(98,mode='s').finalize().extrude(-33))