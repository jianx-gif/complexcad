import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-31,0))
w1=cq.Workplane('ZX',origin=(0,-78,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-73,46),(-53,37)).arc((-35,-46),(47,-31)).segment((67,-40)).segment((73,-24)).segment((53,-16)).arc((35,47),(-37,42)).segment((-67,54)).close().assemble(),mode='s').finalize().extrude(62).union(w1.sketch().circle(40).circle(35,mode='s').finalize().extrude(156))