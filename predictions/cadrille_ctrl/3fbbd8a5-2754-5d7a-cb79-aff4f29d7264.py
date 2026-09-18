import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((2,-15),(15,0),(2,15)).close().assemble().finalize().extrude(36).union(w0.sketch().segment((-40,-11),(-38,-11)).arc((0,-40),(38,-11)).segment((40,-11)).segment((40,11)).segment((38,11)).arc((0,40),(-38,11)).segment((-40,11)).close().assemble().reset().face(w0.sketch().segment((-24,-1),(0,-21)).segment((24,1)).segment((0,21)).close().assemble(),mode='s').push([(27,1)]).circle(4,mode='s').finalize().extrude(60)).union(w0.sketch().circle(39).circle(20,mode='s').finalize().extrude(60))
