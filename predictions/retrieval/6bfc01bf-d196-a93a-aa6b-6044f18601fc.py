import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    stem_width=30.0,
    stem_thickness=8.0,
    stem_height=60.0,
    flange_width=70.0,
    flange_thickness=10.0,
    rib_width=6.0,
    rib_thickness=3.0
)

stem = cq.Workplane('XY').box(m.stem_width, m.stem_thickness, m.stem_height).translate((0,0,m.stem_height/2))
flange = cq.Workplane('XY').box(m.flange_width, m.stem_thickness, m.flange_thickness).translate((0,0,m.stem_height+m.flange_thickness/2))
rib = cq.Workplane('XY').box(m.rib_width, m.rib_thickness, m.stem_height*0.6).translate((0, -(m.stem_thickness/2 + m.rib_thickness/2), m.stem_height*0.3))
result = stem.union(flange).union(rib)
