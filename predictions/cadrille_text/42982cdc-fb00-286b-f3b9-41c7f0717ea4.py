import cadquery as cq
w0=cq.Workplane('XY',origin=(-30,-30,-100))
r=w0.sketch().segment((-25,25),(25,25)).arc((0,30),(-25,25)).assemble().reset().face(w0.sketch().arc((27,-25),(30,-30),(30,-35)).arc((32,-30),(33,-25)).close().assemble()).finalize().extrude(200)