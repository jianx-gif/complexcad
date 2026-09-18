import cadquery as cq
w0=cq.Workplane('YZ',origin=(-53,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-50,-31),(-12,-26),(20,-45)).segment((20,45)).segment((-50,45)).close().assemble().finalize().extrude(141).union(w1.sketch().arc((-94,20),(0,62),(94,20)).segment((94,27)).arc((0,89),(-94,27)).close().assemble().finalize().extrude(-200))