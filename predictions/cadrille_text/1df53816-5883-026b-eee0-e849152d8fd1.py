import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-2))
w1=cq.Workplane('XY',origin=(-100,0,-2))
r=w0.sketch().circle(3).circle(2,mode='s').finalize().extrude(27).union(w1.sketch().segment((29,-11),(29,11)).arc((27,0),(29,-11)).assemble().finalize().extrude(-59))