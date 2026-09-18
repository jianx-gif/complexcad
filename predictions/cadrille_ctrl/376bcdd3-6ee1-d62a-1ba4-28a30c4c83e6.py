import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,15,0))
r=w0.sketch().segment((-39,-13),(-37,-13)).arc((-1,-40),(35,-13)).segment((39,-13)).segment((39,13)).segment((35,13)).arc((-1,40),(-37,13)).segment((-39,13)).close().assemble().push([(-1,0)]).circle(33,mode='s').finalize().extrude(-1).union(w0.sketch().push([(-1,0)]).circle(39).circle(30,mode='s').finalize().extrude(5))
