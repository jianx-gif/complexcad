import cadquery as cq

outer_radius = 40.0
base_height = 20.0
channel_height = 40.0
channel_start_radius = 12.0
channel_end_radius = 20.0
wall_thickness = 2.0
hole_dia = 5.0
hole_offset = 20.0
chamfer_dist = 1.0

total_height = base_height + channel_height

outer = cq.Workplane("XY").circle(outer_radius).extrude(total_height)

channel_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, base_height)
    .lineTo(channel_start_radius, base_height)
    .lineTo(channel_start_radius, base_height + 10)
    .threePointArc(
        (channel_start_radius + 5, base_height + 15),
        (channel_end_radius, base_height + 20),
    )
    .lineTo(channel_end_radius, total_height)
    .lineTo(0, total_height)
    .close()
    .revolve()
)

part = outer.cut(channel_profile).shell(-wall_thickness)

# Chamfer top outer edge using top face edges
part = part.faces(">Z").edges().chamfer(chamfer_dist)

hole_pts = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
]
part = (
    part.faces(">Z")
    .workplane()
    .pushPoints(hole_pts)
    .hole(hole_dia)
)

result = part