import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-10))
r=w0.sketch().segment((29,-58),(32,-58)).segment((32,-48)).arc((30,-50),(29,-52)).close().assemble().finalize().extrude(-50).union(w0.sketch().push([(30,-10)]).circle(2).push([(30,-9.5)]).rect(2,3,mode='s').finalize().extrude(30)).union(w0.sketch().push([(30,-10)]).circle(2).push([(98,-10)]).rect(4,2).finalize().extrude(79))