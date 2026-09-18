import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-47,0))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().arc((-49,-100),(-29,-91),(-10,-80)).segment((-10,-75)).segment((-4,-75)).arc((1,-74),(7,-74)).arc((29,-58),(49,-37)).segment((49,98)).arc((-52,28),(-49,-100)).assemble().finalize().extrude(78).union(w0.sketch().arc((-16,-82),(2,-74),(16,-60)).arc((40,-46),(55,-21)).arc((45,-20),(35,-18)).arc((20,-40),(-4,-52)).arc((-8,-68),(-16,-82)).assemble().finalize().extrude(94)).union(w1.sketch().push([(35,-3)]).circle(65).circle(15,mode='s').finalize().extrude(42))