import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-95,0))
r=w0.sketch().segment((-100,-67),(-99,-67)).segment((-99,-69)).segment((99,-69)).segment((99,69)).segment((-99,69)).segment((-99,94)).segment((-100,94)).close().assemble().push([(-45,-23)]).circle(28,mode='s').finalize().extrude(-10).union(w0.sketch().arc((-65,-12),(14,-29),(79,17)).close().assemble().finalize().extrude(120)).union(w1.sketch().arc((-59,-17),(0,-52),(59,-17)).segment((50,-17)).arc((0,-47),(-50,-17)).close().assemble().finalize().extrude(189))