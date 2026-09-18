import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
r=w0.sketch().segment((-42,-14),(11,-35)).segment((42,14)).segment((-11,35)).close().assemble().finalize().extrude(1).union(w0.sketch().circle(45).circle(40,mode='s').finalize().extrude(30)).union(w0.sketch().arc((42,-6),(45,0),(42,6)).close().assemble().finalize().extrude(39))
