import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,36))
r=w0.sketch().circle(30).circle(25,mode='s').finalize().extrude(-73).union(w0.sketch().circle(100).circle(96,mode='s').finalize().extrude(-73))