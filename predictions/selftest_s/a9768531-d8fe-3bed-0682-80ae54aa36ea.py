import cadquery as cq

shaft_length = 80.0
shaft_diameter = 30.0
step_length = 30.0
step_diameter = 20.0
reduced_length = 15.0
reduced_diameter = 15.0
key_slot_width = 8.0
key_slot_depth = 4.0
chamfer_distance = 1.0

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_diameter / 2, 0)
    .lineTo(shaft_diameter / 2, step_length)
    .radiusArc((step_diameter / 2, step_length + 10), 15)
    .lineTo(step_diameter / 2, shaft_length)
    .close()
)

main_shaft = profile.revolve(360)

reduction_cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(reduced_diameter / 2)
    .extrude(reduced_length)
    .edges()
    .chamfer(chamfer_distance)
    .translate((0, 0, shaft_length - reduced_length / 2))
)

shaft_with_reduction = main_shaft.cut(reduction_cylinder)

key_slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(key_slot_width, key_slot_depth)
    .extrude(shaft_length)
)

result = shaft_with_reduction.cut(key_slot)
