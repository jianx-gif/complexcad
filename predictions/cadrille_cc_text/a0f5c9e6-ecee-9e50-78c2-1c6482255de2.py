import cadquery as cq
hub_outer_radius = 45.0
hub_inner_radius = 20.0
hub_half_length = 15.0
root_fillet_radius = 3.0
keyway_width = 6.0
keyway_depth = 10.0
chamfer_distance = 0.5
fillet_radius = 2.0
hole_dia = 5.0
hole_angle_spacing = 120.0
hole_count = 6
hole_radius = hub_outer_radius - 5.0
base = (
    cq.Workplane("XZ")
    .moveTo(hub_half_radius, 0)
    .lineTo(hub_half_radius, hub_half_length)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length + keyway_depth)
    .lineTo(hub_half_radius, hub_half_length)
    .lineTo(hub_half_radius, hub_half_length)
    .lineTo(hub_half_radius, 0)
    .close()
    .revolve(360)
)
result = (
    base
    .edges()
    .chamfer(chamfer_distance)
)
