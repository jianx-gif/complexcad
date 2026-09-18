import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,41,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,29)]).circle(69).circle(60,mode='s').finalize().extrude(-111).union(w0.sketch().segment((-35,-29),(-33,-31)).segment((35,29)).segment((33,31)).close().assemble().finalize().extrude(50)).union(w1.sketch().arc((-99,-32),(0,-82),(99,-32)).segment((57,-32)).arc((0,-64),(-57,-32)).close().assemble().finalize().extrude(-173))