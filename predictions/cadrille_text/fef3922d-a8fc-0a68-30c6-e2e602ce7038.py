import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-50))
r=w0.sketch().circle(82).circle(81,mode='s').finalize().extrude(100)