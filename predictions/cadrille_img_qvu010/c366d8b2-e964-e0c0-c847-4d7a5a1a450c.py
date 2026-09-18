import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('YZ',origin=(-29,0,0))
r=w0.sketch().arc((-79,-49),(-49,-40),(-22,-25)).arc((-20,-18),(-13,-19)).arc((14,15),(29,56)).close().assemble().finalize().extrude(199).union(w1.sketch().arc((-87,-83),(1,-10),(87,-56)).arc((85,-49),(83,-42)).arc((75,-38),(75,-29)).arc((-17,98),(-87,-37)).close().assemble().finalize().extrude(66))