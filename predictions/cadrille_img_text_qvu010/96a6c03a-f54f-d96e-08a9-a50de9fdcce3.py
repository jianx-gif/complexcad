import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,30,0))
w1=cq.Workplane('ZX',origin=(0,77,0))
r=w0.sketch().arc((-35,33),(25,23),(1,-32)).segment((1,-33)).segment((35,-33)).segment((35,33)).close().assemble().finalize().extrude(-97).union(w0.sketch().circle(100).circle(96,mode='s').finalize().extrude(46)).union(w1.sketch().circle(74).circle(45,mode='s').finalize().extrude(-113))