import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((-50,29),(-49,29)).segment((-49,31)).close().assemble().finalize().extrude(100).union(w0.sketch().push([(0,40)]).circle(12).push([(0,39.5)]).rect(18,13,mode='s').finalize().extrude(99)).union(w0.sketch().push([(0,40)]).circle(12).push([(0,39.5)]).rect(18,13,mode='s').finalize().extrude(100))