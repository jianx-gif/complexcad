import cadquery as cq
pipe_outer_diameter = 20.0
wall_thickness = 2.0
pipe_inner_diameter = pipe_outer_diameter - 2 * wall_thickness
pipe_outer_radius = pipe_outer_diameter / 2.0
wall_thickness = wall_thickness
keyway_width = 4.0
keyway_depth = 3.0
keyway_length = pipe_outer_radius - wall_thickness
chamfer_size = 0.5
outer_radius = pipe_outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, pipe_outer_radius)
    .lineTo(pipe_outer_radius, pipe_outer_radius)
    .lineTo(pipe_outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
