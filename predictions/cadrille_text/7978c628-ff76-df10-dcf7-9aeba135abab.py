import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-10))
w1=cq.Workplane('XY',origin=(-100,-100,-10))
r=w0.sketch().circle(3).circle(2,mode='s').finalize().extrude(110).union(w1.sketch().segment((29,-8),(29,8)).arc((27,0),(29,-8)).assemble().finalize().extrude(20))