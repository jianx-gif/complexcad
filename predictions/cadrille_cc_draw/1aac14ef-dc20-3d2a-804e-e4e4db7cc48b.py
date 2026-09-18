import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    plate_width=60.0,
    plate_depth=30.0,
    plate_thickness=4.0,
    rib_width=12.0,
    rib_height=15.0,
    rib_thickness=2.0,
    rib_spacing=15.0,
    rib_count=4,
    rib_rows=2,
    rib_cols=4,
    rib_rows=2,
    rib_rows=4,
    rib_cols=4,
    rib_cols=4,
    rib_cols=2,
    rib_cols=2,
    rib_cols=2,
    rib_cols=3,
    rib_cols=3,
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
        (m.leg_width, 0),
        (m.leg_width, m.leg_depth),
        (m.leg_width, m.leg_depth),
        (0, m.leg_depth),
        (0, 0)
    ])
    .close()
    .extrude(m.rib_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
result = base.union(rib)
