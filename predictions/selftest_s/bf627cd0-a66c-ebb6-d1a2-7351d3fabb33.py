import cadquery as cq

hub_base_radius = 15
hub_top_radius = 25
hub_length = 30
flange_thickness = 5
flange_outer_radius = 45
bore_radius = 8
key_slot_width = 6
key_slot_depth = 4
hole_radius = 3
hole_pattern_radius = 35
fillet_radius = 2
chamfer_distance = 1

result = (
    cq.Workplane('XZ')
    .polyline([
        (0, 0),
        (hub_base_radius, 0),
        (hub_top_radius, hub_length),
        (hub_top_radius + flange_thickness, hub_length),
        (hub_top_radius + flange_thickness, flange_outer_radius),
        (0, flange_outer_radius)
    ])
    .close()
    .revolve(360)
)

bore = cq.Workplane('XY').circle(bore_radius).extrude(flange_outer_radius + 10)
result = result.cut(bore)

slot = (
    cq.Workplane('YZ')
    .center(0, hub_length / 2)
    .rect(key_slot_width, hub_length)
    .extrude(key_slot_depth)
    .translate((hub_top_radius - key_slot_depth, 0, 0))
)
result = result.cut(slot)

hole_positions = [
    (hole_pattern_radius, 0),
    (0, hole_pattern_radius),
    (-hole_pattern_radius, 0),
    (0, -hole_pattern_radius)
]
for x, y in hole_positions:
    result = result.faces('>Z').workplane().center(x, y).hole(2 * hole_radius)

result = result.edges('|Z').fillet(fillet_radius)
result = result.edges('>Z').chamfer(chamfer_distance)
