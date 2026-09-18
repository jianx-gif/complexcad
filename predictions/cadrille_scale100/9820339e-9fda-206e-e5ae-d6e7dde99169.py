import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().arc((24,-18),(24,-16),(26,-16)).arc((25,-15),(24,-15)).close().assemble().finalize().extrude(-21).union(w0.sketch().arc((24,-18),(24,-1),(30,14)).arc((-29,6),(24,-18)).assemble().push([(0,-1)]).circle(2,mode='s').finalize().extrude(-20))