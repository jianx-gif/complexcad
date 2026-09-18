import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,18))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().push([(1,0)]).circle(20).circle(20,mode='s').finalize().extrude(-18).union(w0.sketch().push([(1,0)]).circle(40).circle(35,mode='s').finalize().extrude(2)).union(w1.sketch().push([(1,0)]).circle(20).circle(20,mode='s').finalize().extrude(-20))
