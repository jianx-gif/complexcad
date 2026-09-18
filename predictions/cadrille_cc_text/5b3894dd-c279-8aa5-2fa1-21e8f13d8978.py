import cadquery as cq
outer_radius = 35.0
inner_radius_step1 = 20.0
inner_radius_step2 = 15.0
step_height = 60.0
step_height = 15.0
hole_diameter = 4.0
hole_center_radius = 24.0
outer_chamfer = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, step_height)
    .lineTo(inner_radius_step1, step_height)
    .lineTo(inner_radius_step2, step_height)
    .lineTo(outer_radius_step2, step_height)
    .lineTo(outer_radius, step_height)
    .lineTo(inner_radius, step_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(outer_chamfer)
hole_cylinder = (
    cq.Workplane("XY")
    .circle(hole_diameter / 2)
    .extrude(hole_center_radius)
)
solid = solid.cut(hole_cylinder)
solid = solid.edges().chamfer(outer_chamfer)
result = solid
