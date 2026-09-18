import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-40,-30),(-29,-30)).segment((-29,-22)).arc((-35,-26),(-40,-22)).close().assemble().finalize().extrude(-5).union(w0.sketch().segment((-40,-19),(39,-30)).segment((40,-19)).arc((40,-18),(41,-17)).segment((40,-17)).segment((40,19)).segment((39,30)).segment((-39,30)).close().assemble().finalize().extrude(-5)).union(w0.workplane(offset=-5/2).moveTo(0,-1).cylinder(5,14))
