import cadquery as cq
plate_width = 80.0
plate_height = 30.0
plate_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset_from_end = 10.0
chamfer_distance = 0.5
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
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (-hole_spacing/2, -hole_offset_from_end),
    (hole_spacing/2, -hole_offset_from_end),
    (-hole_spacing/2, hole_offset_from_end),
    (hole_spacing/2, hole_offset_from_end)
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
