import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,22)]).circle(59).circle(14,mode='s').push([(56,32)]).circle(11,mode='s').finalize().extrude(23).union(w1.sketch().arc((-80,-54),(-1,-39),(80,-54)).segment((80,-33)).arc((22,12),(-19,74)).arc((-48,61),(-80,54)).segment((-80,33)).arc((-22,0),(-80,-33)).close().assemble().finalize().extrude(-200))