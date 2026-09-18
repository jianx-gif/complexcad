import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
height = 60.0
wall_thickness = 10.0
inner_radius = inner_radius + wall_thickness
chamfer = 0.8
vent_slot_width = 12.0
vent_slot_height = 30.0
vent_slot_depth = wall_thickness + 2.0
hole_diameter = 5.0
hole_angle_offset = 0.0
hole_center_height = 45.0
rib_thickness = 2.0
rib_height = 5.0
rib_length = outer_radius - wall_thickness
rib_count = int(360 / rib_count)
rib_count = int(rib_length / rib_count)
rib_profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .close()
)
result = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_length, rib_height)
    .translate((outer_radius + rib_thickness / 2, 0, 0))
)
result = result.cut(rib_profile)
hole_positions = [
    (hole_center_radius * math.cos(math.radians(i * 360 / hole_angle_offset)),
    (hole_center_radius * math.sin(math.radians(i * 360 / hole_angle_offset)),
    (hole_center_radius * math.sin(math.radians(i * 360 / hole_angle_offset)),
    (hole_center_radius * math.sin(math.radians(i * 360 / hole_angle_offset)),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter / 2)
    .cutBlind(-hole_depth)
)
result = result.edges("|Z").chamfer(chamfer)
