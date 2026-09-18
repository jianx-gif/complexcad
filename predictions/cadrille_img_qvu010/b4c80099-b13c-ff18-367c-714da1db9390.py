import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-27,0))
w1=cq.Workplane('ZX',origin=(0,-35,0))
r=w0.sketch().circle(100).circle(85,mode='s').finalize().extrude(43).union(w1.sketch().circle(85).reset().face(w1.sketch().segment((-11,-11),(-1,-11)).segment((-1,-17)).segment((1,-17)).segment((1,-11)).segment((11,-11)).segment((11,11)).segment((1,11)).segment((1,17)).segment((-1,17)).segment((-1,11)).segment((-11,11)).close().assemble(),mode='s').finalize().extrude(122))