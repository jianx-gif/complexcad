import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,67,0))
r=w0.sketch().circle(34).reset().face(w0.sketch().segment((-21,13),(-16,11)).arc((-7,-19),(18,-1)).segment((21,-3)).segment((21,-1)).segment((16,1)).arc((7,18),(-11,18)).segment((-20,18)).close().assemble(),mode='s').finalize().extrude(-134).union(w0.workplane(offset=-14/2).cylinder(14,100))