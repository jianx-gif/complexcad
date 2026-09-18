import cadquery as cq
rail_length = 80.0
rail_radius = 20.0
wall_thickness = 5.0
lip_height = 10.0
lip_extra_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
counterbore_diameter = 6.0
counterbore_depth = 2.0
slot_width = 2.0
slot_length = rail_length - 2 * wall_thickness
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (rail_radius, 0),
        (rail_radius, rail_length),
        (0, rail_length),
    ])
    .close()
    .revolve()
)
result = (
    profile
    .faces(">Z")
    .workplane()
    .circle(rail_length - 2 * wall_thickness)
    .extrude(rail_length)
    .faces(">Z")
    .workplane()
    .circle(rail_length - 2 * wall_thickness)
    .cutBlind(-wall_thickness)
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_offset, startAngle=0, angle=360, count=hole_spacing)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_length)
    .edges("|Z")
    .chamfer(chamfer_size)
)
