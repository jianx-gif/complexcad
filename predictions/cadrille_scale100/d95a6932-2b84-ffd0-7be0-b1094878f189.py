import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((28,-29),(28,-25)).arc((-30,23),(32,-20)).segment((36,-20)).arc((-33,23),(28,-29)).assemble().finalize().extrude(-1).union(w0.sketch().circle(40).circle(38,mode='s').finalize().extrude(100))