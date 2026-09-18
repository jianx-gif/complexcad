import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 6.0
corner_radius = 8.0
chamfer_size = 1.0
hole_diameter = 6.0
hole_depth = 4.0
hole_spacing_x = 30.0
hole_spacing_y = 25.0
rib_width = 20.0
rib_height = 15.0
rib_thickness = 3.0
rib_fillet = 2.0

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .edges(">Z")
    .chamfer(chamfer_size)
)

rib = (
    base.faces("<Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .edges("|Z")
    .fillet(rib_fillet)
)

combined = base.union(rib)

hole_positions = [
    (-hole_spacing_x, -hole_spacing_y/2),
    (0, -hole_spacing_y/2),
    (hole_spacing_x, -hole_spacing_y/2),
    (-hole_spacing_x, hole_spacing_y/2),
    (0, hole_spacing_y/2),
    (hole_spacing_x, hole_spacing_y/2),
]

result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)
