import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
w1=cq.Workplane('ZX',origin=(0,6,0))
r=w0.sketch().segment((-40,-20),(39,-20)).segment((39,20)).segment((-40,20)).segment((-40,14)).arc((-39,13),(-40,12)).close().assemble().finalize().extrude(-8).union(w0.sketch().segment((-35,-19),(35,-19)).segment((35,19)).segment((-35,19)).segment((-35,12)).arc((-32,11),(-35,10)).close().assemble().finalize().extrude(-8)).union(w0.workplane(offset=12/2).moveTo(26,3).cylinder(12,5)).union(w1.sketch().segment((-20,20),(20,20)).arc((0,40),(-20,20)).assemble().finalize().extrude(-6))