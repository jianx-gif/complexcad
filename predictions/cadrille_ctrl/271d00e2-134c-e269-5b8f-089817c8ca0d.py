import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-60/2).moveTo(0,-1).cylinder(60,2).union(w0.sketch().segment((-29,-10),(-28,-10)).arc((0,-30),(28,-10)).segment((29,-10)).segment((29,-7)).arc((30,0),(29,7)).segment((29,10)).segment((28,10)).arc((0,30),(-28,10)).segment((-29,10)).segment((-29,7)).arc((-30,0),(-29,-7)).close().assemble().push([(22,-1)]).circle(4,mode='s').finalize().extrude(58)).union(w0.sketch().segment((-26,13),(-1,-25)).segment((26,-13)).segment((1,25)).close().assemble().finalize().extrude(60))
