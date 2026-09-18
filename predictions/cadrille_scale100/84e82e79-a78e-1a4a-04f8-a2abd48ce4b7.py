import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().circle(12).circle(11,mode='s').finalize().extrude(-15).union(w0.sketch().circle(40).circle(12,mode='s').finalize().extrude(-14)).union(w0.sketch().circle(46).circle(10,mode='s').finalize().extrude(-8))