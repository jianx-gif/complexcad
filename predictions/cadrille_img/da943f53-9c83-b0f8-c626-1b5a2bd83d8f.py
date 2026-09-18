import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-44,0))
w1=cq.Workplane('ZX',origin=(0,-37,0))
r=w0.sketch().push([(11,12)]).circle(88).circle(27,mode='s').finalize().extrude(10).union(w0.sketch().segment((-79,16),(41,-76)).segment((79,-25)).segment((-41,76)).close().assemble().finalize().extrude(14)).union(w1.sketch().push([(11,12)]).circle(88).reset().face(w1.sketch().segment((1,-1),(14,-1)).arc((52,33),(5,17)).segment((1,17)).close().assemble(),mode='s').finalize().extrude(-20))