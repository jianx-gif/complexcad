import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-83))
r=w0.workplane(offset=-17/2).cylinder(17,82).union(w0.sketch().circle(73).reset().face(w0.sketch().segment((-69,23),(-49,1)).arc((-36,-35),(-2,-50)).segment((18,-72)).segment((69,-23)).segment((49,-1)).arc((36,35),(2,50)).segment((-18,72)).close().assemble(),mode='s').finalize().extrude(183))