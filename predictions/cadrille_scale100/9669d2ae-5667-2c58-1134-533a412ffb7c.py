import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
w1=cq.Workplane('ZX',origin=(0,1,0))
r=w0.sketch().circle(85).circle(8,mode='s').finalize().extrude(-55).union(w0.sketch().segment((-82,-27),(-77,-27)).arc((0,-85),(77,-27)).segment((82,-27)).segment((82,27)).segment((77,27)).arc((0,85),(-77,27)).segment((-82,27)).close().assemble().finalize().extrude(5)).union(w1.sketch().segment((-2,-6),(2,-6)).segment((2,-1)).arc((1,0),(2,1)).segment((2,6)).segment((-2,6)).close().assemble().finalize().extrude(-40))