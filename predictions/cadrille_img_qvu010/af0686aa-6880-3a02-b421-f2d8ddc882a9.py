import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('XY',origin=(0,0,59))
r=w0.sketch().circle(100).circle(71,mode='s').circle(42).finalize().extrude(38).union(w1.sketch().arc((-85,21),(-79,51),(-63,78)).arc((-85,-49),(40,-91)).arc((38,-89),(37,-87)).arc((-73,-47),(-85,21)).assemble().finalize().extrude(-119))