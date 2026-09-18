import cadquery as cq

outer_diameter = 80.0
spacer_height = 20.0
wall_thickness = 8.0
outer_edge_radius = 2.0
chamfer_distance = 0.5
blind_hole_diameter = 20.0
blind_hole_depth = 12.0
slot_width = 8.0
slot_depth = 10.0
slot_count = 6
boss_radius = 10.0
boss_height = 6.0
mount_hole_diameter = 5.0
mount_hole_center_radius = 30.0

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(spacer_height)
    .edges(">Z")
    .fillet(outer_edge_radius)
    .shell(-wall_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(blind_hole_diameter / 2)
    .cutBlind(blind_hole_depth)
    .faces(">Z")
    .workplane()
    .polarArray(
        radius=outer_diameter / 2 - slot_depth / 2 - wall_thickness,
        angle=360 / slot_count,
        count=slot_count,
        startAngle=0,
    )
    .rect(slot_width, slot_depth)
    .cutBlind(spacer_height)
    .faces("<Z")
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
    .faces(">Z")
    .workplane()
    .polarArray(
        radius=mount_hole_center_radius,
        angle=90,
        count=4,
        startAngle=0,
    )
    .hole(mount_hole_diameter)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
