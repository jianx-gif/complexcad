import cadquery as cq

rail_length = 80
rail_radius = 20
wall_thickness = 5
lip_height = 10
lip_extra_thickness = 2
chamfer_size = 1
hole_diameter = 4
hole_spacing = 20
hole_offset = 10
hole_count = 3
slot_width = 2
slot_length = rail_length * 0.6
counterbore_diameter = 6
counterbore_depth = 2

profile_points = [
    (rail_radius, 0),
    (rail_radius + wall_thickness, 0),
    (rail_radius + wall_thickness, rail_length - lip_height),
    (rail_radius + wall_thickness + lip_extra_thickness, rail_length - lip_height),
    (rail_radius + wall_thickness + lip_extra_thickness, rail_length),
    (rail_radius, rail_length)
]

result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve(360)
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

slot = (
    cq.Workplane("XZ")
    .center(rail_radius - slot_width / 2, (rail_length - slot_length) / 2)
    .rect(slot_width, slot_length)
    .extrude(wall_thickness * 2)
)
result = result.cut(slot)

hole_positions = [hole_offset + i * hole_spacing for i in range(hole_count)]
for z in hole_positions:
    through_hole = (
        cq.Workplane("XY")
        .circle(hole_diameter / 2)
        .extrude(wall_thickness + lip_extra_thickness + 2)
        .translate((rail_radius + wall_thickness / 2, 0, z))
    )
    result = result.cut(through_hole)
    counterbore = (
        cq.Workplane("XY")
        .circle(counterbore_diameter / 2)
        .extrude(counterbore_depth)
        .translate((rail_radius + wall_thickness + counterbore_depth / 2, 0, z))
    )
    result = result.cut(counterbore)
