import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-75,-6),(-27,-6)).arc((-29,0),(-27,6)).segment((-75,6)).close().assemble().reset().face(w0.sketch().segment((27,-6),(75,-6)).segment((75,6)).segment((27,6)).arc((29,0),(27,-6)).assemble()).finalize().extrude(200)