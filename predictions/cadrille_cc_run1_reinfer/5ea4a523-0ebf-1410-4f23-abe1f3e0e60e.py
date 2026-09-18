import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, rib_width)
    .extrude(rib_height)
)
rib = rib.union(rib)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, rib_width)
    .extrude(plate_thickness)
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset),
    (-hole_spacing/2, -hole_offset),
    (hole_spacing/2, -hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
