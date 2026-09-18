import cadquery as cq
plate_width = 80.0
plate_height = 60.0
plate_thickness = 20.0
wall_thickness = 2.0
rib_width = 4.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_x = 10.0
hole_offset_y = 15.0
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_height)
    .translate((0, 0, plate_thickness))
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing/2, -hole_offset_x),
    (hole_spacing/2, -hole_offset_y),
    (-hole_spacing/2, hole_offset_y),
    (hole_spacing/2, hole_offset_y),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
