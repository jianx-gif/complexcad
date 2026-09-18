import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-40,0))
w1=cq.Workplane('YZ',origin=(-10,0,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-60,-31),(-17,-66)).segment((-17,-68)).segment((-15,-68)).segment((-10,-72)).segment((-7,-68)).segment((17,-68)).segment((17,-42)).arc((44,-26),(55,4)).arc((88,41),(45,66)).arc((32,72),(17,75)).segment((17,68)).segment((-17,68)).segment((-17,42)).arc((-44,15),(-45,-23)).close().assemble(),mode='s').finalize().extrude(136).union(w1.sketch().push([(-1,0)]).circle(99).circle(55,mode='s').finalize().extrude(-46))