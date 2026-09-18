import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,33,0))
r=w0.sketch().arc((-16,-90),(12,-7),(96,1)).arc((-63,71),(-16,-90)).assemble().finalize().extrude(-162).union(w1.sketch().circle(97).circle(89,mode='s').finalize().extrude(-133))