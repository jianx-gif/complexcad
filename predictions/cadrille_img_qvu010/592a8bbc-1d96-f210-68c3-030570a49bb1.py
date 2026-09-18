import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('ZX',origin=(0,-77,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(35).union(w1.sketch().arc((45,-67),(50,-62),(55,-58)).arc((-49,60),(45,-67)).assemble().finalize().extrude(154))