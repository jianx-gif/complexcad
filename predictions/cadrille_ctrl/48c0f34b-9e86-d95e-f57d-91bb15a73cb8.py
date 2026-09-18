import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,21))
w1=cq.Workplane('ZX',origin=(0,17,0))
r=w0.sketch().segment((-29,1),(-27,1)).segment((-29,2)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-17,10),(-15,10)).segment((-15,11)).segment((-17,11)).close().assemble().finalize().extrude(-21)).union(w0.sketch().segment((-17,10),(-15,10)).segment((-15,11)).segment((-17,11)).segment((-17,10)).assemble().finalize().extrude(-21)).union(w0.sketch().segment((-16,10),(-15,10)).segment((-15,11)).segment((-16,11)).arc((-15,12),(-16,13)).close().assemble().finalize().extrude(-21)).union(w0.sketch().segment((-15,-11),(-12,-11)).segment((-12,-12)).segment((-13,-12)).arc((26,13),(-15,-11)).assemble().finalize().extrude(-17))
