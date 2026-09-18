import cadquery as cq

outer_diameter = 80.0
wall_thickness = 2.0
tube_length = 70.0
flange_height = 10.0
flange_extension = 5.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_count = 12

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, tube_length - flange_height)
    .lineTo(outer_radius + flange_extension, tube_length)
    .lineTo(inner_radius + flange_extension, tube_length)
    .lineTo(inner_radius, tube_length - flange_height)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
    .edges()
    .chamfer(chamfer_distance)
)

result = base
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    hole = (
        cq.Workplane("YZ")
        .center(outer_radius - wall_thickness / 2.0, 0)
        .circle(hole_diameter / 2.0)
        .extrude(wall_thickness * 2.0)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.cut(hole)
