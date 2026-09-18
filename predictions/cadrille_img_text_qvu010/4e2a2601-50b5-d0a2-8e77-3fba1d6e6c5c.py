import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-92))
w1=cq.Workplane('YZ',origin=(-63,0,0))
r=w0.sketch().segment((-95,-16),(-53,69)).arc((-86,31),(-95,-16)).assemble().finalize().extrude(192).union(w1.sketch().arc((-94,-45),(-61,-31),(-34,-10)).arc((-28,61),(29,23)).arc((43,23),(54,22)).arc((55,23),(56,23)).arc((57,24),(58,24)).arc((58,66),(34,100)).segment((-43,100)).arc((-44,98),(-45,100)).segment((-46,100)).arc((-87,45),(-94,-20)).close().assemble().finalize().extrude(147))