import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('ZX',origin=(0,-13,0))
r=w0.sketch().arc((-93,34),(-1,-1),(49,-89)).arc((59,-73),(66,-55)).segment((51,-61)).arc((-1,-1),(-51,60)).segment((-36,66)).segment((-36,67)).segment((-51,61)).arc((-59,73),(-66,89)).arc((-79,62),(-93,34)).assemble().finalize().extrude(116).union(w1.sketch().arc((-23,82),(10,-82),(23,84)).segment((23,89)).arc((10,-85),(-23,86)).close().assemble().finalize().extrude(27))