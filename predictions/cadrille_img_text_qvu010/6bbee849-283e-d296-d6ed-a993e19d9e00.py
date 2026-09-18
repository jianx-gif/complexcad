import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-85,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-89,-16),(-79,-17),(-70,-22)).arc((1,45),(7,-53)).arc((37,-42),(60,-21)).segment((89,16)).segment((70,32)).arc((49,62),(15,76)).segment((-4,93)).segment((-33,61)).arc((-67,30),(-89,-10)).close().assemble().finalize().extrude(170).union(w1.sketch().arc((-100,-12),(0,-93),(100,-12)).segment((94,-12)).arc((0,-85),(-94,-12)).close().assemble().finalize().extrude(200))