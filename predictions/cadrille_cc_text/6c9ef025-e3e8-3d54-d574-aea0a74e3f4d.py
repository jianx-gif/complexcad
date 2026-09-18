import cadquery as cq
pipe_od = 30.0
pipe_base_radius = 40.0
pipe_angle_deg = 60.0
flange_length = 10.0
flange_extra_radius = 5.0
fillet_radius = 1.0
hole_diameter = 4.0
hole_count = 6
hole_spacing = pipe_base_radius + flange_length / 2.0
hole_positions = [(-hole_count - 1) * hole_spacing, 0) for i in range(hole_count)]
flange = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(pipe_base_radius, 0)
    .lineTo(pipe_base_radius, pipe_base_radius)
    .lineTo(pipe_base_radius + flange_length, pipe_base_radius)
    .lineTo(pipe_base_radius + flange_length, pipe_base_radius)
    .lineTo(pipe_base_radius, pipe_base_radius)
    .close()
    .revolve()
)
solid = flange.union(flange)
solid = solid.edges().fillet(fillet_radius)
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter/2)
    .extrude(hole_depth)
)
solid = solid.edges().fillet(fillet_radius)
result = solid
