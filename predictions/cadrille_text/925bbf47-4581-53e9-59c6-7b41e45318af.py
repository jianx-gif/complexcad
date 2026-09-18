import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-100,-3))
r=w0.sketch().segment((-53,96),(-48,96)).segment((-53,97)).close().assemble().finalize().extrude(10).union(w0.sketch().push([(0,100)]).circle(5).push([(0,99.5)]).rect(4,3,mode='s').finalize().extrude(13))