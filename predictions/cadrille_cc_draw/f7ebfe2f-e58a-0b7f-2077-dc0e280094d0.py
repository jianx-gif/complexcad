import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_width=80.0,
    outer_depth=60.0,
    wall_thickness=10.0,
    rib_width=30.0,
    rib_height=15.0,
    rib_thickness=5.0,
    rib_spacing=12.0,
    rib_count=8,
    rib_rows=2,
    rib_cols=2,
    rib_rows=2,
    rib_spacing=15.0,
    rib_spacing=15.0,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
)
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.outer_width, 0),
        (m.outer_width, m.outer_depth),
        (m.outer_width, m.outer_depth),
        (0, m.outer_depth),
        (0, 0)
    ])
    .close()
    .extrude(m.rib_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(0, m.rib_spacing)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
result = base.union(rib)
