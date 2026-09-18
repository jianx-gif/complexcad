import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-18,0))
w1=cq.Workplane('ZX',origin=(0,-19,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(64).union(w1.sketch().arc((-64,12),(-33,-61),(46,-66)).arc((50,-64),(53,-61)).arc((61,-52),(67,-42)).arc((26,69),(-64,12)).assemble().finalize().extrude(-63))