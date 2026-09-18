import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-40,-30),(-12,-30)).segment((-12,-21)).arc((-26,-26),(-40,-21)).close().assemble().finalize().extrude(8).union(w0.sketch().segment((-40,-1),(-12,-1)).arc((-26,-6),(-40,-1)).assemble().reset().face(w0.sketch().arc((-3,-1),(0,-10),(0,-19)).segment((40,-19)).segment((40,30)).segment((-3,30)).close().assemble()).push([(19,12)]).circle(12,mode='s').finalize().extrude(8)).union(w0.sketch().push([(19,12)]).circle(13).circle(10,mode='s').finalize().extrude(8))
