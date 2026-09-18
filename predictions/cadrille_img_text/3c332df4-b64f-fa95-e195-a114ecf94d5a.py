import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-84,0))
w1=cq.Workplane('XY',origin=(0,0,81))
r=w0.sketch().segment((-100,-58),(-99,-58)).segment((-100,-57)).close().assemble().reset().face(w0.sketch().segment((-100,-49),(75,58)).segment((100,58)).segment((100,59)).segment((53,78)).segment((53,58)).segment((-29,58)).arc((-53,49),(-77,58)).segment((-100,58)).close().assemble()).finalize().extrude(182).union(w1.sketch().segment((-48,-81),(48,-81)).segment((48,-29)).arc((0,-53),(-48,-29)).close().assemble().finalize().extrude(-141))