import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-67,-10),(-63,-19)).segment((-62,-19)).arc((10,-62),(63,4)).segment((67,5)).segment((63,14)).segment((62,14)).arc((-10,62),(-63,-8)).close().assemble().circle(50,mode='s').finalize().extrude(-200).union(w0.workplane(offset=-15/2).cylinder(15,67))