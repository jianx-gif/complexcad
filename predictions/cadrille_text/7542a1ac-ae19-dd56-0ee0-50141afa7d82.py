import cadquery as cq
w0=cq.Workplane('XY',origin=(-78,-57,-100))
r=w0.sketch().segment((-71,77),(-67,77)).segment((-67,81)).close().assemble().reset().face(w0.sketch().segment((23,-58),(27,-58)).segment((27,-54)).close().assemble()).finalize().extrude(200)