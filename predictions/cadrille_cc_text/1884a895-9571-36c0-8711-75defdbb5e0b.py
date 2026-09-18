import cadquery as cq
plate_width = 30.0
plate_thickness = 4.0
num_teeth = 20
hole_diameter = 6.0
hole_spacing_x = 20.0
hole_spacing_y = 20.0
chamfer_distance = 1.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(plate_width, 0)
    .lineTo(plate_width, plate_thickness)
    .lineTo(plate_width - hole_spacing_x, plate_thickness)
    .lineTo(plate_width - hole_spacing_y, plate_thickness + 2)
    .lineTo(plate_width, plate_thickness + 2)
    .lineTo(0, plate_thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, -hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter / 2)
    .cutBlind(-hole_depth)
)
result = solid
