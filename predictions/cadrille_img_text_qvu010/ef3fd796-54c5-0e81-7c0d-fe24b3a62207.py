import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-84,-6),(-29,-6)).arc((-31,0),(-29,6)).segment((-84,6)).arc((-82,0),(-84,-6)).assemble().reset().face(w0.sketch().segment((29,-6),(84,-6)).segment((84,6)).segment((29,6)).arc((31,0),(29,-6)).assemble()).finalize().extrude(-200)