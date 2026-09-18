import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-73))
r=w0.sketch().segment((-99,-16),(-97,-16)).arc((0,-100),(97,-16)).segment((99,-16)).segment((99,16)).segment((97,16)).arc((0,100),(-97,16)).segment((-99,16)).close().assemble().circle(73,mode='s').finalize().extrude(-27).union(w0.workplane(offset=105/2).cylinder(105,40)).union(w0.workplane(offset=173/2).cylinder(173,20))