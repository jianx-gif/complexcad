import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,50))
r=w0.sketch().circle(30).push([(-22,-13)]).circle(2,mode='s').finalize().extrude(-150).union(w0.sketch().segment((-50,3),(-43,0)).arc((-18,-41),(28,-39)).segment((35,-42)).segment((50,-3)).segment((43,0)).arc((18,41),(-28,39)).segment((-35,42)).close().assemble().finalize().extrude(-38)).union(w0.workplane(offset=50/2).cylinder(50,30))