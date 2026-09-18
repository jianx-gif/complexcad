import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-40))
w1=cq.Workplane('XY',origin=(0,0,-45))
r=w0.sketch().segment((-68,13),(-30,13)).segment((-30,-57)).segment((30,-57)).segment((30,13)).segment((68,13)).segment((68,26)).segment((30,26)).segment((30,100)).segment((-30,100)).segment((-30,26)).segment((-68,26)).close().assemble().finalize().extrude(-5).union(w1.sketch().push([(0,-10)]).circle(90).push([(33,-46)]).circle(11,mode='s').finalize().extrude(90))