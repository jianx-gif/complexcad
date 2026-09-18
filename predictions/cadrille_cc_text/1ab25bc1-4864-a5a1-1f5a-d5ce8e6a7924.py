import cadquery as cq
outer_radius = 40.0
base_height = 20.0
channel_start_radius = 12.0
channel_height = 40.0
wall_thickness = 2.0
hole_dia = 5.0
hole_offset = 20.0
chamfer_dist = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, channel_height)
    .lineTo(channel_start_radius, channel_height)
    .lineTo(channel_start_radius, channel_height + channel_height)
    .lineTo(0, channel_height + channel_height)
    .close()
)
solid = profile.revolve()
solid = solid.shell(wall_thickness)
solid = solid.faces(">Z").edges().chamfer(chamfer_dist)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_dia)
)
solid = (
    solid.faces(">Z").workplane()
    .circle(hole_dia / 2)
    .extrude(wall_thickness + 2)
)
solid = solid.cut(hole_positions)
result = solid
