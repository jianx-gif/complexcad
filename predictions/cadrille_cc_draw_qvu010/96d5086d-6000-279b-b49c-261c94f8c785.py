import cadquery as cq
plate_width = 80.0
plate_height = 20.0
plate_thickness = 10.0
rib_height = 6.0
rib_width = 12.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_from_end = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_height)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing / 2, -hole_offset_from_end),
    (hole_spacing / 2, -hole_offset_from_end),
    (-hole_spacing / 2, hole_offset_from_end),
    (hole_spacing / 2, hole_offset_from_end)
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (0, 1), (0, 0)])
    .hole(hole_diameter)
)
result = combined
