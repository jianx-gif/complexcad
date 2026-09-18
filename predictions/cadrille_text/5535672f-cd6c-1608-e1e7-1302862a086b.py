import cadquery as cq
w0=cq.Workplane('XY',origin=(-93,0,-56))
w1=cq.Workplane('XY',origin=(-100,-8,-56))
r=w0.sketch().segment((-47,10),(-47,12)).segment((-45,12)).arc((-49,11),(-45,10)).close().assemble().finalize().extrude(113).union(w1.sketch().segment((29,-8),(35,-8)).segment((35,-4)).arc((32,-6),(29,-4)).close().assemble().finalize().extrude(112))