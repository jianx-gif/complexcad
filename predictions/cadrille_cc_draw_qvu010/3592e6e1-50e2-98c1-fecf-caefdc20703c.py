import cadquery as cq
base_length = 100.0
base_width = 30.0
base_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_end = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (-base_length/2 + hole_offset_from_end + i * hole_spacing,
    (-base_length/2 + hole_offset_from_end + j * hole_spacing),
    (base_length/2 - hole_offset_from_end + j * hole_spacing)/2,
    (-base_length/2 + hole_offset_from_end + j * hole_spacing)/2,
]
for x, y in hole_positions:
    combined = (
        combined
        .faces(">Z")
        .workplane()
        .pushPoints(hole_positions)
        .hole(hole_diameter)
    )
result = combined
