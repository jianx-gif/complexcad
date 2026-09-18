import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.workplane(offset=-34/2).moveTo(-40,26).cylinder(34,60).union(w1.sketch().arc((-39,-11),(-38,-12),(-38,-13)).arc((-1,-33),(39,-34)).arc((40,-34),(40,-33)).arc((43,-32),(45,-31)).arc((48,-30),(50,-29)).arc((54,-27),(58,-24)).arc((59,-24),(59,-23)).arc((61,19),(45,59)).arc((3,51),(-33,70)).arc((-35,69),(-37,67)).arc((-37,68),(-38,68)).arc((-67,28),(-39,-11)).assemble().finalize().extrude(200))