import cadquery as cq
outer_diameter = 80.0
wall_thickness = 2.0
channel_length = 100.0
channel_width = 4.0
notch_width = 5.0
notch_height = 10.0
notch_depth = wall_thickness + 2.0
hole_diameter = 4.0
countersink_diameter = 8.0
countersink_angle = 90.0
chamfer_size = 0.5
rib_width = 6.0
rib_height = 12.0
rib_spacing = 25.0
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, channel_length)
    .lineTo(0, channel_length)
    .close()
    .revolve()
)
notch = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(notch_depth)
    .extrude(channel_width)
    .translate((0, 0, channel_length - channel_width))
)
notch = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(notch_depth)
    .extrude(channel_width)
    .translate((0, 0, channel_length - channel_width))
)
result = base.cut(notch)
result = result.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
result = result.union(rib)
result = result.edges().chamfer(chamfer_size)
result = result.edges().chamfer(chamfer_size)
