import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=6/2).box(80,60,6).union(w0.sketch().segment((-40,-30),(40,-30)).segment((40,30)).segment((-40,30)).segment((-40,26)).segment((-36,26)).segment((-36,-26)).segment((-40,-26)).close().assemble().finalize().extrude(14)).union(w0.sketch().segment((-36,-13),(-24,-13)).arc((-25,0),(-24,13)).segment((-36,13)).close().assemble().reset().face(w0.sketch().segment((24,-13),(36,-13)).segment((36,13)).segment((24,13)).arc((25,0),(24,-13)).assemble()).finalize().extrude(14))
