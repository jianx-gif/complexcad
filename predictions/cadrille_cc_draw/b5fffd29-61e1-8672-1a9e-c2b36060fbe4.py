import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 10.0
rib_height = 5.0
rib_width = 12.0
rib_spacing = 15.0
rib_count = 6
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width - 2 * rib_spacing)
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
    (-hole_spacing/2, hole_spacing/2),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
