import cadquery as cq
channel_total_length = 80.0
channel_outer_radius = 20.0
channel_inlet_radius = 30.0
step_height = 5.0
wall_thickness = 4.0
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = channel_inlet_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(channel_outer_radius, 0)
    .lineTo(channel_outer_radius, channel_total_length - step_height)
    .lineTo(channel_outer_radius + step_height, channel_total_length - step_height)
    .lineTo(channel_outer_radius + step_height, channel_total_length)
    .lineTo(channel_outer_radius + step_height, channel_total_length)
    .lineTo(channel_outer_radius, channel_total_length)
    .lineTo(0, channel_total_length)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360).hole(mount_hole_diameter)
result = solid
