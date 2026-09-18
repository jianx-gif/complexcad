import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-40,-30),(40,-30)).segment((40,30)).segment((-40,30)).segment((-40,19)).arc((-38,18),(-40,17)).close().assemble().circle(10,mode='s').finalize().extrude(-5).union(w0.sketch().segment((-25,-13),(-25,13)).arc((-27,0),(-25,-13)).assemble().reset().face(w0.sketch().arc((-23,-16),(0,-27),(23,-16)).close().assemble()).reset().face(w0.sketch().segment((-23,16),(23,16)).arc((0,27),(-23,16)).assemble()).finalize().extrude(-5))
