import cadquery as cq
from types import SimpleNamespace as Measures

measures = Measures(
    plate_width=80.0,
    plate_depth=60.0,
    plate_thickness=6.0,
    edge_fillet_radius=8.0,
    edge_chamfer=1.0,
    hole_spacing_x=30.0,
    hole_spacing_y=25.0,
    hole_rows=2,
    hole_cols=3,
    hole_diameter=6.0,
    hole_depth=4.0,
    boss_width=20.0,
    boss_depth=15.0,
    boss_height=4.0,
    boss_fillet=2.0
)

m = measures

model = (
    cq.Workplane("XY")
    .box(m.plate_width, m.plate_depth, m.plate_thickness)
    .edges("|Z").fillet(m.edge_fillet_radius)
    .edges(">Z").chamfer(m.edge_chamfer)
    .faces(">Z")
    .workplane()
    .rect(
        (m.hole_cols - 1) * m.hole_spacing_x,
        (m.hole_rows - 1) * m.hole_spacing_y,
        forConstruction=True
    )
    .vertices()
    .hole(m.hole_diameter, depth=m.hole_depth)
    .faces("<Z")
    .workplane(offset=-m.plate_thickness/2 + m.boss_height/2)
    .rect(m.boss_width, m.boss_depth)
    .extrude(m.boss_height)
    .edges("|Z")
    .fillet(m.boss_fillet)
)

result = model