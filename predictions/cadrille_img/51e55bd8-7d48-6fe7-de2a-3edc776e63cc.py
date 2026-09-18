import cadquery as cq
w0=cq.Workplane('YZ',origin=(80,0,0))
w1=cq.Workplane('ZX',origin=(0,-50,0))
r=w0.sketch().segment((-18,-84),(18,-84)).segment((18,-79)).arc((79,0),(18,79)).segment((18,84)).segment((-18,84)).segment((-18,79)).arc((-79,0),(-18,-79)).close().assemble().circle(81,mode='s').finalize().extrude(-139).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-12)).union(w1.sketch().push([(0,28)]).circle(69).circle(57,mode='s').finalize().extrude(83))