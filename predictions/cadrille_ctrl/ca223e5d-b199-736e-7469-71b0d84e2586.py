import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,70))
r=w0.sketch().segment((-30,2),(-29,2)).arc((-28,-1),(-27,-4)).segment((-28,-4)).segment((-30,-4)).close().assemble().finalize().extrude(-140).union(w0.sketch().push([(0,0.5)]).rect(58,7).push([(0,0)]).circle(3,mode='s').finalize().extrude(-70)).union(w0.sketch().arc((-14,32),(13,-32),(-9,34)).arc((-11,29),(-14,32)).assemble().push([(0,0)]).circle(28,mode='s').finalize().extrude(-70))
