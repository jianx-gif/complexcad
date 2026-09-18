import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-66))
w1=cq.Workplane('ZX',origin=(0,-90,0))
r=w0.sketch().segment((-78,80),(-77,77)).segment((-77,79)).segment((-38,79)).arc((-28,81),(-18,79)).segment((11,79)).segment((11,48)).arc((13,40),(14,32)).segment((78,8)).segment((77,11)).segment((77,8)).segment((11,8)).segment((11,-23)).segment((-18,-23)).arc((-28,-25),(-38,-23)).segment((-77,-23)).segment((-77,80)).close().assemble().finalize().extrude(166).union(w1.sketch().segment((-100,-77),(-65,-77)).arc((-92,0),(-65,77)).segment((-100,77)).close().assemble().finalize().extrude(179))