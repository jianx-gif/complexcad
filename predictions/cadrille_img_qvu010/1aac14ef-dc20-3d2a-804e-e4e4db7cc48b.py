import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,45,0))
w1=cq.Workplane('XY',origin=(0,0,-77))
r=w0.sketch().segment((-24,2),(24,-10)).segment((-24,65)).close().assemble().finalize().extrude(-140).union(w0.sketch().segment((-87,-1),(-79,-74)).segment((65,-57)).segment((44,74)).segment((-31,63)).arc((-53,19),(-87,-1)).assemble().push([(-11,0)]).circle(22,mode='s').finalize().extrude(-15)).union(w1.sketch().segment((-100,0),(-95,0)).arc((-69,52),(-33,95)).arc((-69,61),(-100,20)).close().assemble().finalize().extrude(177))