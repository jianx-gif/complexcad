import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
w1=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().arc((-39,-11),(-35,-11),(-38,-14)).arc((39,12),(-39,-11)).assemble().finalize().extrude(-2).union(w0.sketch().arc((-39,-10),(39,-10),(-35,19)).segment((-35,-10)).close().assemble().finalize().extrude(8)).union(w1.workplane(offset=-10/2).cylinder(10,45))
