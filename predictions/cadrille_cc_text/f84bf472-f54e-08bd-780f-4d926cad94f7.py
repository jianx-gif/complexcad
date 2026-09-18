import cadquery as cq
pipe_outer_diameter = 12.0
pipe_inner_diameter = 10.0
pipe_wall_thickness = 2.0
flange_extra_radius = 10.0
flange_thickness = 4.0
counterbore_diameter = 13.0
counterbore_depth = 5.0
counterbore_radius = pipe_outer_diameter / 2.0
hole_offset = 5.0
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(pipe_outer_diameter / 2.0, 0)
    .lineTo(pipe_outer_diameter / 2.0, pipe_wall_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_extra_radius)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_extra_radius)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_extra_radius)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_extra_radius)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_extra_radius)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + flange_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + fllet_angle)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + Inylinder_angle)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + Inylinder_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + Inylinder_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + Inylinder_thickness)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .lineTo(pipe_inner_diameter / 2.0, pipe_wall_thickness + 0.0)
    .close()
    .revolve()
)
solid = profile