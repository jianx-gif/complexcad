import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    plate_width=30.0,
    plate_depth=10.0,
    plate_thickness=5.0,
    rib_height=12.0,
    rib_thickness=4.0,
    rib_offset_from_end=15.0,
    hole_diameter=4.0,
    hole_spacing=12.0,
    hole_offset_from_end=10.0
)
base = (
    cq.Workplane("XY")
    .rect(m.plate_width, m.plate_depth)
    .extrude(m.plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(m.rib_thickness, m.rib_height)
    .extrude(m.rib_height)
)
rib = rib.translate((0, 0, m.plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(m.chamfer)
combined = combined.faces(">Z").workplane().hole(m.hole_diameter)
combined = (
    combined.faces(">Z").workplane()
    .center(m.hole_offset_from_end, 0)
    .hole(m.hole_diameter)
)
combined = (
    combined.faces(">Z").workplane()
    .center(m.hole_offset_from_end, 0)
    .hole(m.hole_diameter)
)
result = combined
