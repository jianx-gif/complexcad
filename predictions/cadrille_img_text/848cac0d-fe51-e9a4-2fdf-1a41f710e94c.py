import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-49,-66),(0,-81),(49,-66)).close().assemble().reset().face(w0.sketch().segment((-49,66),(49,66)).arc((0,81),(-49,66)).assemble()).finalize().extrude(114).union(w0.sketch().arc((-44,81),(-35,74),(-26,67)).arc((-33,75),(-44,81)).assemble().reset().face(w0.sketch().arc((44,-59),(59,-50),(69,-37)).arc((57,-49),(44,-59)).assemble()).finalize().extrude(157)).union(w1.sketch().arc((-2,-68),(1,-66),(3,-69)).arc((10,69),(-2,-68)).assemble().finalize().extrude(159))