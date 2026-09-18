import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-31,0))
r=w0.sketch().push([(13,14)]).circle(87).circle(76,mode='s').circle(42).finalize().extrude(29).union(w0.sketch().arc((-46,83),(-39,85),(-32,87)).arc((39,-86),(-27,89)).arc((-29,90),(-31,91)).arc((39,-85),(-46,83)).assemble().finalize().extrude(62))