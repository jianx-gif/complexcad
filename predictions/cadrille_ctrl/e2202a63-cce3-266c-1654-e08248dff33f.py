import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
w1=cq.Workplane('XY',origin=(0,0,40))
r=w0.workplane(offset=-31/2).cylinder(31,30).union(w0.sketch().segment((-29,-9),(-10,-29)).segment((-1,-19)).arc((19,-13),(20,7)).segment((29,17)).segment((10,29)).segment((1,19)).arc((-19,13),(-20,-7)).close().assemble().finalize().extrude(40)).union(w1.sketch().circle(21).circle(2,mode='s').finalize().extrude(-110))
