import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,17))
r=w0.sketch().segment((-100,18),(-99,18)).segment((-99,20)).close().assemble().finalize().extrude(-34).union(w0.sketch().push([(0,1)]).circle(4).push([(0,0.5)]).rect(4,3,mode='s').finalize().extrude(-33))