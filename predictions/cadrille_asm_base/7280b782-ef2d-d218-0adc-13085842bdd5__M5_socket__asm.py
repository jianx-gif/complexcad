import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,82))
w1=cq.Workplane('XY',origin=(0,0,74))
r=w0.sketch().circle(11).reset().face(w0.sketch().segment((-10,-2),(-5,-8)).segment((10,2)).segment((5,8)).close().assemble(),mode='s').finalize().extrude(-182).union(w0.workplane(offset=-8/2).cylinder(8,19)).union(w1.workplane(offset=26/2).cylinder(26,7))