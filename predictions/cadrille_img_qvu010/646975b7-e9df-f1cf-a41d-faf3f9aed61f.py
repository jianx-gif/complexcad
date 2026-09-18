import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-66,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(100).circle(94,mode='s').finalize().extrude(135).union(w1.sketch().arc((-38,-68),(0,-81),(38,-68)).segment((34,-68)).arc((0,-78),(-34,-68)).close().assemble().reset().face(w1.sketch().segment((-38,68),(-34,68)).arc((0,78),(34,68)).segment((38,68)).arc((0,81),(-38,68)).assemble()).reset().face(w1.sketch().arc((39,-66),(81,0),(39,66)).segment((39,28)).arc((40,0),(39,-28)).close().assemble()).finalize().extrude(200))