import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-83,-10))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-57)).arc((31,-57),(29,-58)).assemble().finalize().extrude(95).union(w0.sketch().push([(100,0)]).circle(100).circle(5,mode='s').finalize().extrude(20))