import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().arc((-24,-32),(-23,-32),(-23,-33)).arc((-22,-33),(-21,-32)).close().assemble().finalize().extrude(-60).union(w0.workplane(offset=-30/2).cylinder(30,40)).union(w0.sketch().circle(40).circle(20,mode='s').finalize().extrude(-2))