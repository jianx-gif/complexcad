import cadquery as cq
w0=cq.Workplane('YZ',origin=(-83,0,0))
w1=cq.Workplane('XY',origin=(0,0,-66))
r=w0.sketch().arc((-91,-26),(-79,-31),(-67,-35)).arc((-58,-19),(-46,-5)).arc((-68,11),(-91,26)).close().assemble().reset().face(w0.sketch().arc((31,17),(41,5),(46,-10)).arc((51,-11),(56,-13)).arc((58,4),(53,20)).arc((42,17),(31,17)).assemble()).finalize().extrude(167).union(w1.sketch().segment((-100,-26),(-96,-26)).arc((-98,-22),(-100,-18)).close().assemble().finalize().extrude(166))