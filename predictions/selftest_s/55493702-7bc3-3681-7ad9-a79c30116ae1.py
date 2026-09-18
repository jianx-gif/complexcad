import cadquery as cq

panel_length = 80.0
panel_width = 50.0
panel_thickness = 20.0
wall_thickness = 2.0
chamfer_dist = 0.5

channel_width = 30.0
channel_depth_start = 12.0
channel_depth_end = 6.0
channel_margin = 5.0
channel_start_center_z = panel_thickness - channel_depth_start/2.0

counterbore_dia = 6.0
counterbore_large_dia = 10.0
counterbore_large_depth = 8.0

mount_hole_dia = 4.0
mount_spacing = 20.0

rib_height = 4.0
rib_thickness = 3.0
rib_width = 20.0

# outer solid
outer = cq.Workplane("XY").box(panel_length, panel_width, panel_thickness, centered=(True, True, False))
# inner cavity
inner = (
    cq.Workplane("XY")
    .box(panel_length - 2 * wall_thickness, panel_width - 2 * wall_thickness, panel_thickness - 2 * wall_thickness, centered=(True, True, False))
    .translate((0, 0, wall_thickness))
)
# hollow panel
hollow = outer.cut(inner)
result = (
    hollow
    .edges("|Z")
    .chamfer(chamfer_dist)
    .faces("<X")
    .workplane()
    .center(0, channel_start_center_z)
    .rect(channel_width, channel_depth_start)
    .extrude(
        panel_length - 2 * channel_margin,
        taper=(channel_depth_end - channel_depth_start) / (panel_length - 2 * channel_margin),
    )
    .faces(">X")
    .workplane()
    .center(0, channel_start_center_z)
    .cboreHole(counterbore_dia, counterbore_large_dia, panel_thickness, counterbore_large_depth)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Y")
    .workplane(offset=-wall_thickness/2)
    .pushPoints([(-panel_width/2 + mount_spacing, 0), (panel_width/2 - mount_spacing, 0)])
    .hole(mount_hole_dia)
)
