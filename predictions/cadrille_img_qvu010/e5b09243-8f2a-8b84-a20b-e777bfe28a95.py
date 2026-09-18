import cadquery as cq
w0=cq.Workplane('YZ',origin=(-21,0,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-75,-29),(-69,-29)).arc((-1,-71),(69,-29)).segment((75,-29)).segment((75,-17)).arc((79,10),(75,37)).segment((75,49)).segment((69,49)).arc((-1,91),(-69,49)).segment((-75,49)).segment((-75,37)).arc((-79,10),(-75,-17)).close().assemble().push([(0,10)]).circle(49,mode='s').finalize().extrude(68).union(w1.sketch().arc((-100,22),(-1,-1),(100,22)).segment((100,42)).arc((-1,100),(-100,42)).close().assemble().finalize().extrude(198))