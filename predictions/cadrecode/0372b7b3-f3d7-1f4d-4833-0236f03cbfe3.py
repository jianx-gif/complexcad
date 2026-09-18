import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-45))
w1=cq.Workplane('XY',origin=(0,0,-36))
r=w0.sketch().arc((-16,32),(-10,-35),(20,26)).arc((5,32),(-16,32)).assemble().push([(19,10)]).circle(7,mode='s').finalize().extrude(-54).union(w0.sketch().circle(99).circle(90,mode='s').finalize().extrude(124)).union(w0.sketch().circle(83).circle(59,mode='s').finalize().extrude(144)).union(w1.workplane(offset=123/2).cylinder(123,90))