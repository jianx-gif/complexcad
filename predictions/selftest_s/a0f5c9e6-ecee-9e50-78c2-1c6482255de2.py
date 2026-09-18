import cadquery as cq
import math

hub_outer_radius = 45.0
hub_inner_radius = 20.0
hub_half_length = 15.0
hub_full_length = hub_half_length * 2
root_fillet_radius = 3.0
keyway_width = 6.0
keyway_depth = 10.0
keyway_offset = hub_inner_radius + keyway_depth / 2.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_dia = 5.0
hole_angle_spacing = 120.0
hole_radius = hub_outer_radius - 5.0

profile = (
    cq.Workplane("YZ")
    .moveTo(0, -hub_half_length)
    .lineTo(hub_inner_radius, -hub_half_length)
    .threePointArc((hub_inner_radius + 5, -hub_half_length + 3), (hub_inner_radius + 10, -hub_half_length + 8))
    .lineTo(hub_outer_radius, -hub_half_length + 10)
    .threePointArc((hub_outer_radius + 3, -hub_half_length + 12), (hub_outer_radius, -hub_half_length + 15))
    .lineTo(hub_outer_radius, hub_half_length - 5)
    .threePointArc((hub_outer_radius, hub_half_length - 12), (hub_outer_radius - 5, hub_half_length - 8))
    .lineTo(hub_inner_radius + 10, hub_half_length - 10)
    .lineTo(hub_inner_radius, hub_half_length)
    .close()
)

hub = profile.revolve(360, (0, 0, 1))

hub = hub.edges().filter(lambda e: e.geomType() == "CIRCLE" and abs(e.radius() - hub_outer_radius) < 0.01).fillet(root_fillet_radius)

keyway = (
    cq.Workplane("XY")
    .center(keyway_offset, 0)
    .box(keyway_depth, hub_full_length, keyway_width)
)
hub = hub.cut(keyway)

hub = hub.faces(">Z").edges().chamfer(chamfer_distance)

hole_positions = []
for i in range(3):
    angle = math.radians(i * hole_angle_spacing)
    x = hole_radius * math.cos(angle)
    y = hole_radius * math.sin(angle)
    hole_positions.append((x, y))

hub = (
    hub.faces("|Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints(hole_positions)
    .hole(hole_dia)
)

result = hub