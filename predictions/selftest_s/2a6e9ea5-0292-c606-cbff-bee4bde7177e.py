import cadquery as cq

# Dimensions (max 100 units)
channel_total_length = 80.0
channel_outer_radius = 20.0
channel_inlet_radius = 30.0
channel_taper_length = 15.0
step_height = 5.0
step_extra = 2.0
wall_thickness = 4.0
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = wall_thickness + 1.0

# Outer profile
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(channel_outer_radius, 0)
    .lineTo(channel_inlet_radius, channel_taper_length)
    .lineTo(channel_inlet_radius, channel_total_length - step_height)
    .lineTo(channel_inlet_radius + step_extra, channel_total_length - step_height)
    .lineTo(channel_inlet_radius + step_extra, channel_total_length)
    .lineTo(0, channel_total_length)
    .close()
    .revolve()
)

# Inner profile (offset inward by wall thickness)
inner_outer_radius = channel_outer_radius - wall_thickness
inner_inlet_radius = channel_inlet_radius - wall_thickness
inner_profile = (
    cq.Workplane("XZ")
    .moveTo(inner_outer_radius, 0)
    .lineTo(inner_inlet_radius, channel_taper_length)
    .lineTo(inner_inlet_radius, channel_total_length - step_height)
    .lineTo(inner_inlet_radius + step_extra, channel_total_length - step_height)
    .lineTo(inner_inlet_radius + step_extra, channel_total_length)
    .lineTo(0, channel_total_length)
    .close()
    .revolve()
)

# Subtract inner from outer to create hollow channel
hollow_body = outer_profile.cut(inner_profile)

# Apply chamfer on a representative sharp edge (safety bevel)
hollow_body = hollow_body.edges().first().chamfer(chamfer_distance)

# Add a side mounting hole at mid‑length
hollow_body = (
    hollow_body
    .workplane(offset=0)
    .center(channel_outer_radius - mount_hole_offset, channel_total_length/2)
    .hole(mount_hole_diameter)
)

result = hollow_body
