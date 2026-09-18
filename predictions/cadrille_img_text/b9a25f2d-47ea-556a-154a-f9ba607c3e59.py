import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,59,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-74,-66),(-68,-53),(-63,-40)).segment((-74,-40)).close().assemble().reset().face(w0.sketch().segment((-74,4),(-63,4)).arc((-68,17),(-74,29)).close().assemble()).finalize().extrude(-70).union(w1.sketch().arc((-59,-59),(-49,-57),(-39,-55)).arc((11,35),(24,-66)).arc((33,-67),(42,-68)).arc((11,74),(-59,-59)).assemble().finalize().extrude(-34))