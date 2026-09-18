import cadquery as cq

# Parameters
pulley_outer_radius = 45.0
pulley_hub_radius = 15.0
pulley_width = 20.0
rib_width = 5.0
rib_height = 3.0
groove_angle = 45.0
groove_depth = 8.0
set_screw_diameter = 3.0
set_screw_head_diameter = 6.0
set_screw_head_depth = 2.0
set_screw_depth = 10.0
set_screw_offset = 7.0

half_width = pulley_width / 2.0

# Base pulley with rib via revolve of a 2D profile
base_profile = (
    cq.Workplane("XZ")
    .moveTo(pulley_hub_radius, -half_width)
    .lineTo(pulley_hub_radius, -half_width + rib_height)
    .lineTo(pulley_hub_radius + rib_width, -half_width + rib_height)
    .lineTo(pulley_hub_radius + rib_width, -half_width)
    .lineTo(pulley_outer_radius, -half_width)
    .lineTo(pulley_outer_radius, half_width)
    .lineTo(pulley_hub_radius + rib_width, half_width)
    .lineTo(pulley_hub_radius + rib_width, half_width - rib_height)
    .lineTo(pulley_hub_radius, half_width - rib_height)
    .close()
    .revolve()
)

# V‑groove as a triangular wedge cutting into the outer radius
groove_wedge = (
    cq.Workplane("XZ")
    .moveTo(0, -half_width)
    .lineTo(-groove_depth, 0)
    .lineTo(0, half_width)
    .close()
    .extrude(pulley_outer_radius * 2)  # extrude along Y
    .translate((pulley_outer_radius, 0, 0))
)

after_groove = base_profile.cut(groove_wedge)

# Set screw thread cylinder (axis along X)
thread_cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(set_screw_diameter / 2)
    .extrude(set_screw_depth)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((-pulley_outer_radius + set_screw_offset, 0, 0))
)

# Set screw head counterbore cylinder (larger diameter, shallower depth)
head_cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(set_screw_head_diameter / 2)
    .extrude(set_screw_head_depth)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((-pulley_outer_radius + set_screw_offset, 0, 0))
)

after_screw = after_groove.cut(head_cylinder).cut(thread_cylinder)

result = after_screw
