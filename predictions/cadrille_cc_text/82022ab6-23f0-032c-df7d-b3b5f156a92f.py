import cadquery as cq
vertical_height = 80.0
horizontal_height = 60.0
leg_thickness = 12.0
flange_thickness = 8.0
hole_diameter = 5.0
hole_count = 6
hole_spacing = (vertical_height - flange_thickness) / 2.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_thickness, 0)
    .lineTo(leg_thickness, horizontal_length)
    .lineTo(leg_thickness + flange_thickness, horizontal_length)
    .lineTo(leg_thickness + flange_thickness, horizontal_length - flange_thickness)
    .lineTo(leg_thickness, horizontal_length - flange_thickness)
    .lineTo(leg_thickness, horizontal_length)
    .lineTo(0, horizontal_length)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
hole_positions = [
    (hole_count, 0),
    (-hole_spacing, 0),
    (0, hole_spacing),
    (0, -hole_spacing),
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter / 2.0)
    .cut(hole_spacing)
)
result = solid
