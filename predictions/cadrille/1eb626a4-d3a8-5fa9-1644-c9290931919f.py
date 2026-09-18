import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-88))
w1=cq.Workplane('XY',origin=(0,0,-81))
r=w0.workplane(offset=-12/2).cylinder(12,68).union(w0.sketch().segment((-57,-2),(-51,-2)).arc((-4,-41),(44,-2)).segment((57,-2)).segment((57,2)).segment((44,2)).arc((-4,46),(-51,2)).segment((-57,2)).close().assemble().push([(-4,0)]).circle(41,mode='s').finalize().extrude(188)).union(w1.workplane(offset=181/2).moveTo(-4,0).cylinder(181,44))