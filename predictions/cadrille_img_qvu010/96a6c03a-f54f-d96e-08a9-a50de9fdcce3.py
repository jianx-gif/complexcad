import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,21,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().arc((-21,-1),(10,16),(1,-18)).arc((15,-21),(29,-17)).arc((30,-15),(32,-15)).arc((15,21),(-21,-1)).assemble().finalize().extrude(-97).union(w0.sketch().circle(100).reset().face(w0.sketch().arc((-95,17),(91,-29),(-89,38)).arc((-96,29),(-95,17)).assemble(),mode='s').finalize().extrude(55)).union(w1.sketch().circle(74).circle(49,mode='s').finalize().extrude(-73))