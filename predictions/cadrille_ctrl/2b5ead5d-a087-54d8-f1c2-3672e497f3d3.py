import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-18/2).box(80,40,18).union(w0.sketch().segment((-15,-15),(-15,15)).arc((-19,0),(-15,-15)).assemble().reset().face(w0.sketch().arc((15,-15),(19,0),(15,15)).close().assemble()).finalize().extrude(6)).union(w0.sketch().segment((-15,-15),(15,-15)).segment((15,15)).segment((-15,15)).segment((-15,14)).arc((-13,12),(-15,11)).close().assemble().finalize().extrude(18))
