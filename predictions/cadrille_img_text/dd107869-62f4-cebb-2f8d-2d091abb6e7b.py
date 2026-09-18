import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-58,-29),(1,-1),(58,30)).segment((18,41)).segment((18,88)).segment((-58,88)).close().assemble().finalize().extrude(100).union(w1.sketch().arc((-53,-41),(-35,-46),(-18,-50)).arc((-16,-65),(-11,-79)).segment((-11,-50)).arc((25,-46),(53,-27)).segment((53,-41)).segment((45,-41)).arc((0,-53),(-45,-41)).close().assemble().finalize().extrude(-192))