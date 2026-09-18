import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,18))
r=w0.sketch().segment((-35,-15),(35,-15)).segment((35,15)).segment((-35,15)).segment((-35,10)).arc((-34,9),(-35,8)).close().assemble().finalize().extrude(-18).union(w0.sketch().segment((-40,10),(-35,7)).arc((-18,-36),(27,-30)).segment((31,-32)).segment((40,-10)).segment((35,-7)).arc((18,36),(-27,30)).segment((-31,32)).close().assemble().circle(20,mode='s').finalize().extrude(-10)).union(w0.workplane(offset=-10/2).cylinder(10,40))
