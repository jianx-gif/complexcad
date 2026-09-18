import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-19,0))
w1=cq.Workplane('XY',origin=(0,0,-83))
r=w0.sketch().segment((-100,-74),(-83,-74)).arc((-92,0),(-58,74)).segment((-100,74)).close().assemble().reset().face(w0.sketch().arc((-53,76),(-1,82),(51,67)).segment((51,98)).segment((-53,98)).close().assemble()).reset().face(w0.sketch().arc((58,74),(82,28),(78,-24)).arc((93,32),(58,74)).assemble()).finalize().extrude(11).union(w1.sketch().arc((-79,-12),(0,-62),(79,-12)).segment((78,-12)).arc((0,-59),(-78,-12)).close().assemble().finalize().extrude(183))