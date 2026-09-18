import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-67))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().segment((-100,1),(-93,1)).arc((-57,-70),(22,-78)).segment((18,-78)).segment((18,-67)).arc((-57,60),(72,-11)).segment((85,-11)).segment((85,-1)).segment((92,-1)).segment((92,1)).segment((85,1)).segment((85,11)).segment((78,11)).arc((0,85),(-78,11)).segment((-100,11)).close().assemble().finalize().extrude(167).union(w1.sketch().arc((-97,-24),(72,68),(-57,-82)).arc((-43,-70),(-41,-51)).arc((59,53),(-76,-1)).arc((-90,-10),(-97,-24)).assemble().finalize().extrude(-39))