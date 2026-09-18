import cadquery as cq
base_length = 60.0
base_width = 30.0
base_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_end = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing/2, -hole_offset_from_end),
    (hole_spacing/2, -hole_offset_from_end),
    (-hole_spacing/2, hole_offset_from_end),
    (hole_spacing/2, hole_offset_from_end)
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
