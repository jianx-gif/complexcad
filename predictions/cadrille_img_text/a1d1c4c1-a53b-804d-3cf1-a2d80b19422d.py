import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,21,0))
r=w0.sketch().segment((1,3),(1,5)).arc((0,7),(1,9)).segment((1,11)).segment((3,11)).arc((5,12),(7,11)).segment((9,11)).segment((9,9)).arc((10,7),(9,5)).segment((9,3)).segment((9,1)).segment((7,1)).arc((5,0),(3,1)).segment((1,1)).segment((1,3)).close().assemble().finalize().extrude(200).union(w1.sketch().push([(13,11)]).circle(87).circle(86,mode='s').finalize().extrude(-42))