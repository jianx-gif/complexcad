import cadquery as cq
plate_width = 80.0
plate_depth = 80.0
plate_thickness = 5.0
rib_height = 12.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (0, hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
