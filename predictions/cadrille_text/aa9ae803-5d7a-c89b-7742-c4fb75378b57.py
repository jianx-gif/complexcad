import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-100,36),(-99,36)).segment((-99,38)).close().assemble().reset().face(w0.sketch().segment((25,-58),(27,-56)).segment((25,-54)).close().assemble()).finalize().extrude(200)