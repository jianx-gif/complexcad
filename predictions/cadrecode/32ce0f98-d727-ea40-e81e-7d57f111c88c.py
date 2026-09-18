import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,48))
w1=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().push([(-5,0)]).circle(19).circle(15,mode='s').finalize().extrude(-148).union(w0.sketch().segment((-20,1),(16,-15)).segment((24,1)).segment((-16,17)).close().assemble().finalize().extrude(45)).union(w0.workplane(offset=52/2).moveTo(0,-2).cylinder(52,11)).union(w1.workplane(offset=-141/2).moveTo(-5,0).cylinder(141,15))