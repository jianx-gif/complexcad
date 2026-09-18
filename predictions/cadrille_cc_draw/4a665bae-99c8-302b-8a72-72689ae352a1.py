import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    plate_width=50.0,
    plate_depth=30.0,
    plate_thickness=10.0,
    rib_height=12.0,
    rib_width=12.0,
    rib_depth=6.0,
    rib_count=4,
    rib_margin=1.0,
    rib_spacing=15.0,
    rib_height=10.0,
    rib_offset=15.0
)
base = (
    cq.Workplane("XY")
    .rect(m.plate_width, m.plate_depth)
    .extrude(m.plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_depth)
    .translate((0, 0, m.plate_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(m.chamfer_distance)
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(m.plate_width/2 - m.rib_offset, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_depth)
)
