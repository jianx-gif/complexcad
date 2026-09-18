import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    plate_width=70.0,
    plate_depth=30.0,
    plate_thickness=8.0,
    rib_width=12.0,
    rib_height=20.0,
    rib_thickness=5.0,
    rib_spacing=15.0,
    rib_count=4,
    rib_rows=2,
    rib_cols=2,
    rib_rows=2,
    rib_rows=2,
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
    rib_cols=2,
    rib_cols=2,
)
base = cq.Workplane("XY").polyline(m.rib_width, m.rib_height).close().extrude(m.rib_thickness)
rib = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
rib = rib.edges("|Z").chamfer(m.chamfer)
rib = rib.edges("|Z").chamfer(m.chamfer)
rib = (
    rib.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
result = rib
