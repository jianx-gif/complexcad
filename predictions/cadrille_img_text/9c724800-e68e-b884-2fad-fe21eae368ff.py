import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-28,-59),(16,-47),(53,-22)).close().assemble().finalize().extrude(108).union(w1.sketch().arc((-97,-55),(-29,-40),(30,-70)).arc((38,-66),(46,-61)).arc((-11,-39),(-53,5)).segment((-53,11)).segment((-58,11)).arc((-7,66),(53,19)).arc((68,19),(83,18)).arc((-15,70),(-97,-55)).assemble().finalize().extrude(-200))