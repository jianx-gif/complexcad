import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
w1=cq.Workplane('ZX',origin=(0,-86,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((4,5),(10,5)).arc((29,-10),(48,5)).segment((54,5)).segment((54,12)).segment((48,12)).arc((29,27),(10,12)).segment((4,12)).close().assemble(),mode='s').finalize().extrude(-58).union(w0.workplane(offset=114/2).cylinder(114,43)).union(w1.sketch().circle(57).circle(15,mode='s').finalize().extrude(98))