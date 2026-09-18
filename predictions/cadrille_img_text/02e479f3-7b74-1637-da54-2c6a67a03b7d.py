import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('ZX',origin=(0,28,0))
r=w0.sketch().segment((-61,-48),(-51,-58)).segment((-43,-51)).arc((49,-59),(60,33)).segment((61,48)).segment((51,58)).segment((43,51)).arc((-49,59),(-60,-33)).close().assemble().finalize().extrude(-58).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(18)).union(w1.sketch().push([(11,15)]).circle(79).circle(72,mode='s').finalize().extrude(-68))