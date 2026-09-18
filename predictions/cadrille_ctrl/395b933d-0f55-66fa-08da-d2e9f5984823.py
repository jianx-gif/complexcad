import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-30,-30),(-27,-30)).arc((-29,-24),(-27,-18)).segment((-30,-18)).close().assemble().reset().face(w0.sketch().segment((27,-30),(30,-30)).segment((30,30)).segment((27,30)).arc((29,24),(30,18)).segment((30,17)).arc((29,14),(27,11)).close().assemble()).finalize().extrude(-4).union(w0.sketch().circle(30).circle(27,mode='s').finalize().extrude(30))
