import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-78,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-44,-46),(11,-95),(60,-38)).arc((85,38),(21,95)).arc((29,-21),(-44,-46)).assemble().finalize().extrude(85).union(w0.sketch().circle(95).circle(85,mode='s').finalize().extrude(174)).union(w1.sketch().arc((-44,-43),(-16,-22),(16,-11)).arc((35,18),(65,38)).arc((66,41),(67,43)).arc((-59,38),(-44,-43)).assemble().finalize().extrude(33))