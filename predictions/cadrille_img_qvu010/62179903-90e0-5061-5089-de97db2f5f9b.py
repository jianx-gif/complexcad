import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-51,0))
w1=cq.Workplane('ZX',origin=(0,-59,0))
r=w0.workplane(offset=-4/2).moveTo(0,-3).cylinder(4,97).union(w0.sketch().arc((-89,22),(39,-93),(51,75)).arc((38,89),(22,100)).segment((22,86)).arc((-39,75),(-85,32)).segment((-85,22)).close().assemble().reset().face(w0.sketch().segment((-48,22),(-48,32)).arc((-50,27),(-48,22)).assemble(),mode='s').reset().face(w0.sketch().arc((-47,20),(39,-89),(48,47)).arc((18,-29),(-47,20)).assemble(),mode='s').finalize().extrude(148)).union(w1.workplane(offset=-21/2).moveTo(0,-3).cylinder(21,97))