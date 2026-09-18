import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-25,-100))
w1=cq.Workplane('XY',origin=(-50,-25,-100))
r=w0.sketch().segment((-50,100),(-46,97)).segment((-46,100)).close().assemble().finalize().extrude(200).union(w1.sketch().push([(0,-25)]).rect(10,10).push([(0,45)]).rect(10,10).finalize().extrude(113))