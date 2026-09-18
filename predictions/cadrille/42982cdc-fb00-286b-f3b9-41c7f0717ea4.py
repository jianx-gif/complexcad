import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,75))
w1=cq.Workplane('ZX',origin=(0,12,0))
r=w0.sketch().push([(0,7)]).circle(23).circle(8,mode='s').finalize().extrude(-175).union(w0.sketch().segment((-40,-10),(30,-13)).segment((30,25)).segment((-40,26)).segment((-40,22)).arc((-33,18),(-40,14)).close().assemble().push([(0,7)]).circle(9,mode='s').finalize().extrude(25)).union(w1.sketch().segment((-79,-35),(-65,-35)).arc((-72,-29),(-79,-22)).close().assemble().finalize().extrude(-43))