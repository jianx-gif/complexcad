import cadquery as cq
plate_width = 80.0
plate_depth = 40.0
plate_thickness = 6.0
rib_height = 12.0
rib_width = 12.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_from_end = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .shell(-wall)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, plate_depth, rib_height)
    .translate((0, 0, plate_thickness))
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
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
