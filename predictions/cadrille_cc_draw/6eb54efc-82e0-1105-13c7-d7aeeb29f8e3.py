import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing/2, -hole_offset_from_edge),
    (hole_spacing/2, -hole_offset_from_edge),
    (hole_spacing/2, -hole_offset_from_edge),
    (-hole_spacing/2, -hole_offset_from_edge),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_spacing/2, hole_offset_from_edge)])
    .hole(hole_diameter)
)
