import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
r=w0.sketch().arc((-89,-17),(55,-28),(17,87)).arc((17,78),(15,69)).arc((37,-21),(-55,-17)).close().assemble().finalize().extrude(-199).union(w0.sketch().circle(84).circle(70,mode='s').finalize().extrude(1))