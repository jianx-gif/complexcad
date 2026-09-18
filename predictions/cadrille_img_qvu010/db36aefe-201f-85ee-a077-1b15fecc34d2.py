import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-44,0))
w1=cq.Workplane('ZX',origin=(0,-40,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-34,-21),(29,-29)).segment((34,21)).segment((-29,29)).close().assemble(),mode='s').finalize().extrude(14).union(w0.sketch().arc((-19,-69),(0,-71),(19,-69)).close().assemble().finalize().extrude(111)).union(w1.sketch().segment((-1,-99),(1,-99)).segment((1,-100)).arc((100,0),(1,100)).segment((1,99)).segment((-1,99)).segment((-1,100)).arc((-100,0),(-1,-100)).close().assemble().finalize().extrude(-19))