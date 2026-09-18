import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().push([(0,-1)]).circle(39).circle(37,mode='s').finalize().extrude(-20).union(w0.sketch().segment((-37,-11),(-29,-11)).arc((-31,-10),(-32,-8)).segment((-37,-8)).close().assemble().finalize().extrude(-20))