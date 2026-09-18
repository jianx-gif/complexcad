import cadquery as cq
plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 12
rib_count = 6
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_width, plate_width - 2 * rib_width)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing/2, -hole_spacing/2),
    ( hole_spacing/2, -hole_spacing/2),
    ( hole_spacing/2, hole_spacing/2),
    ( hole_spacing/2, hole_spacing/2),
]
for x, y in hole_positions:
    combined = (
        combined.faces(">Z").workplane()
        .pushPoints(hole_positions)
        .hole(hole_diameter)
    )
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
