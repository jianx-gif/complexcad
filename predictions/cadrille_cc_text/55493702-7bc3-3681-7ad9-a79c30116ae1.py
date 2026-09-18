import cadquery as cq
panel_length = 80.0
panel_width = 50.0
panel_thickness = 20.0
wall_thickness = 2.0
chamfer_dist = 0.5
channel_width = 30.0
channel_depth_start = 12.0
channel_depth_end = 6.0
mount_hole_dia = 6.0
mount_spacing = 20.0
mount_rows = 2
mount_cols = 3
mount_hole_dia = 10.0
mount_hole_radius = (panel_width / 2) - 2 * wall_thickness
rib_width = 20.0
rib_height = 4.0
rib_thickness = 3.0
rib_length = panel_width - 2 * wall_thickness
base = cq.Workplane("XY").box(panel_length, panel_width, panel_thickness)
channel = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(channel_width, channel_depth_start)
    .extrude(panel_thickness)
)
channel = channel.edges("|Z").chamfer(chamfer_dist)
channel = channel.edges().chamfer(chamfer_dist)
channel = channel.edges("|Z").chamfer(chamfer_dist)
channel = (
    channel
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(mount_hole_radius, mount_hole_radius)
    .rarray(mount_spacing, 0, mount_cols, 1)
    .extrude(rib_thickness)
)
channel = channel.edges("|Z").chamfer(chamfer_dist)
channel = channel.edges("|Z").chamfer(chamfer_dist)
result = channel
