import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
outer_height = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
chamfer_size = 1.0
hole_diameter = 4.0
hole_depth = 10.0
hole_count = 6
hole_circle_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_height)
    .lineTo(inner_radius, outer_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = (
    solid.faces(">Z").workplane()
    .circle(inner_radius)
    .extrude(-wall_thickness)
)
solid = solid.faces(">Z").workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
