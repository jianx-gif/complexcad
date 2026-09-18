import cadquery as cq

pipe_center_radius = 30.0
pipe_outer_diameter = 12.0
pipe_wall_thickness = 2.0
elbow_angle = 135.0
counterbore_diameter = 13.0
counterbore_depth = 5.0
socket_shaft_diameter = 8.0
hole_offset = 5.0
chamfer_size = 0.5
flange_extra_radius = 10.0
flange_thickness = 4.0

# Derived dimensions
pipe_inner_diameter = pipe_outer_diameter - 2 * pipe_wall_thickness

# Create rectangular profile for pipe wall offset from axis
profile = (
    cq.Workplane("XZ")
    .moveTo(pipe_center_radius - pipe_outer_diameter / 2.0, 0)
    .lineTo(pipe_center_radius - pipe_outer_diameter / 2.0, pipe_outer_diameter)
    .lineTo(pipe_center_radius + pipe_outer_diameter / 2.0, pipe_outer_diameter)
    .lineTo(pipe_center_radius + pipe_outer_diameter / 2.0, 0)
    .close()
)

# Revolve profile to form elbow segment
elbow = profile.revolve(elbow_angle)

# Flange at inlet (circular plate on start of elbow)
flange_radius = pipe_center_radius + flange_extra_radius
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
)
# Align flange with start of elbow (centered at origin, offset in Z)
flange = flange.translate((0, 0, -flange_thickness / 2))

assembly = elbow.union(flange)

# Counterbore and through hole on inlet side, positioned on flange face
hole_x = pipe_center_radius
hole_y = 0
counterbore = (
    cq.Workplane("XY")
    .center(hole_x, hole_y)
    .circle(counterbore_diameter / 2.0)
    .extrude(-counterbore_depth)
)
shaft_hole = (
    cq.Workplane("XY")
    .center(hole_x, hole_y)
    .circle(socket_shaft_diameter / 2.0)
    .extrude(-20)
)
hole_cut = counterbore.union(shaft_hole)

result = assembly.cut(hole_cut)

result = result.edges(">Z").chamfer(chamfer_size)
