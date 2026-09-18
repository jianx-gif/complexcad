import cadquery as cq
w0=cq.Workplane('YZ',origin=(39,0,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().segment((-39,-58),(-39,-39)).arc((-67,0),(-39,39)).segment((-39,58)).arc((-79,0),(-39,-58)).assemble().reset().face(w0.sketch().arc((39,-58),(79,0),(39,58)).segment((39,39)).arc((67,0),(39,-39)).close().assemble()).finalize().extrude(-77).union(w1.sketch().segment((-39,-30),(-39,30)).segment((39,30)).segment((39,39)).segment((79,39)).arc((-75,37),(11,-79)).arc((29,-44),(67,-30)).close().assemble().finalize().extrude(107))