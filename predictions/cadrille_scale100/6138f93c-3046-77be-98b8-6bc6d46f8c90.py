import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,71))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.workplane(offset=-71/2).cylinder(71,32).union(w0.sketch().segment((-40,-30),(-28,-30)).arc((0,-38),(28,-30)).segment((40,-30)).segment((40,30)).segment((28,30)).arc((0,38),(-28,30)).segment((-40,30)).close().assemble().finalize().extrude(25)).union(w1.sketch().circle(38).circle(36,mode='s').finalize().extrude(-23))