import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-25))
w1=cq.Workplane('ZX',origin=(0,11,0))
r=w0.sketch().segment((-100,-25),(-90,-39)).segment((-64,-22)).arc((-79,-22),(-89,-12)).close().assemble().reset().face(w0.sketch().arc((-74,-10),(-59,-10),(-50,-20)).segment((-24,5)).segment((-34,18)).close().assemble()).finalize().extrude(45).union(w1.sketch().segment((-25,-29),(25,-29)).segment((25,-3)).arc((0,100),(-25,-3)).close().assemble().push([(0,46)]).circle(31,mode='s').finalize().extrude(28))