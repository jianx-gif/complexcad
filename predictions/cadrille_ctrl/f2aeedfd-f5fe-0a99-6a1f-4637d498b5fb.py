import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-40,1),(-36,-11)).segment((-34,-10)).segment((-34,-7)).segment((-35,-7)).segment((-35,-6)).segment((-36,-6)).segment((-36,-5)).segment((-37,-5)).segment((-37,-4)).segment((-38,-4)).segment((-38,-3)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-40,1),(-39,1)).segment((-40,1)).close().assemble().finalize().extrude(-1))
