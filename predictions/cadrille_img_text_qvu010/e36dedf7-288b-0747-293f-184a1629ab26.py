import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('ZX',origin=(0,-82,0))
r=w0.sketch().circle(96).reset().face(w0.sketch().segment((-21,-11),(-17,-21)).segment((21,11)).segment((17,21)).close().assemble(),mode='s').finalize().extrude(10).union(w1.sketch().arc((-99,19),(-97,17),(-95,15)).arc((94,-31),(-87,46)).arc((-94,35),(-99,23)).segment((-96,23)).arc((-95,21),(-94,19)).close().assemble().finalize().extrude(164))