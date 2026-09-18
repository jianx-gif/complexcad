import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,29,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().segment((-1,-86),(1,-86)).segment((1,-79)).arc((79,0),(1,79)).segment((1,86)).segment((-1,86)).segment((-1,79)).arc((-79,0),(-1,-79)).close().assemble().circle(78,mode='s').finalize().extrude(-10).union(w1.sketch().arc((1,-1),(2,-1),(2,-2)).arc((3,-2),(4,-3)).arc((5,2),(1,-1)).assemble().finalize().extrude(-136))