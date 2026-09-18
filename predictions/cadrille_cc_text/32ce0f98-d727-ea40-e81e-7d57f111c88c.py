import cadquery as cq
pipe_outer_radius = 10.0
pipe_thickness = 2.0
inner_radius = pipe_outer_radius - pipe_thickness
inner_radius = inner_radius - pipe_thickness
screw_length = 80.0
fillet_radius = 0.5
clearance = 0.5
clearance = 0.1
clearance = 0.2
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, pipe_thickness)
    .lineTo(inner_radius + pipe_thickness, pipe_thickness)
    .lineTo(inner_radius + pipe_thickness, pipe_thickness + inner_radius)
    .lineTo(inner_radius + pipe_thickness, pipe_thickness + inner_radius)
    .lineTo(inner_radius, pipe_thickness + inner_radius)
    .close()
)
solid = profile.revolve()
solid = solid.shell(-wall_thickness)
solid = solid.faces(">Z").edges().fillet(fillet_radius)
solid = solid.faces(">Z").edges().chamfer(0.5)
solid = solid.faces(">Z").edges().fillet(fillet_radius)
result = solid
