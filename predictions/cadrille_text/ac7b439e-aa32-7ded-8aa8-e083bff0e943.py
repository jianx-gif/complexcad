import cadquery as cq
w0=cq.Workplane('XY',origin=(-11,-100,-50))
r=w0.sketch().segment((28,99),(30,99)).segment((30,100)).close().assemble().finalize().extrude(100).union(w0.sketch().push([(0,9)]).circle(4).circle(3,mode='s').finalize().extrude(100))