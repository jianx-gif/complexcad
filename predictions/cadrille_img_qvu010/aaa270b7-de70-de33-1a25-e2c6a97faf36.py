import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(100).push([(-50,-6)]).circle(18,mode='s').push([(0,0)]).circle(27,mode='s').push([(50,-6)]).circle(21,mode='s').finalize().extrude(-20).union(w1.sketch().arc((-81,-22),(0,-82),(81,-22)).segment((79,-22)).arc((0,-81),(-79,-22)).close().assemble().reset().face(w1.sketch().segment((-81,22),(-79,22)).arc((0,81),(79,22)).segment((81,22)).arc((0,82),(-81,22)).assemble()).finalize().extrude(174))