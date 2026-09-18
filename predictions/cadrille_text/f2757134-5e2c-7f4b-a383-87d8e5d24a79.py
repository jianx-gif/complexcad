import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-5))
w1=cq.Workplane('XY',origin=(-100,-15,-5))
r=w0.sketch().segment((-100,15),(-99,15)).segment((-99,17)).close().assemble().finalize().extrude(105).union(w1.sketch().push([(0,1)]).circle(8).push([(0,0.5)]).rect(10,7,mode='s').finalize().extrude(-51))