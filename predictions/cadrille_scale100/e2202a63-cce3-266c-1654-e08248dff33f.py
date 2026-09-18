import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
w1=cq.Workplane('XY',origin=(0,0,40))
r=w0.workplane(offset=-30/2).cylinder(30,30).union(w0.sketch().segment((-29,-9),(-10,-29)).segment((-1,-19)).arc((18,-11),(19,9)).segment((29,19)).segment((10,29)).segment((1,19)).arc((-18,11),(-19,-9)).close().assemble().finalize().extrude(40)).union(w1.sketch().circle(21).rect(4,36,mode='s').finalize().extrude(30))