import cadquery as cq

outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
wall_thickness = 2.0
height = 20.0
flange_width = 5.0
vent_slot_width = 2.0
vent_slot_length = 12.0
vent_count = 12
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
chamfer_size = 0.5

profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (0, height),
        (outer_radius + flange_width, height),
        (outer_radius + flange_width, height - 5),
        (outer_radius - 5, height - 5),
        (outer_radius - 5, 0)
    ])
    .close()
)
solid = profile.revolve(360)

shelled = solid.shell(wall_thickness)

vented = (
    shelled
    .faces("|Z").first()
    .workplane()
    .polarArray(
        radius=outer_radius - wall_thickness / 2.0,
        startAngle=0,
        count=vent_count,
        angle=360
    )
    .rect(vent_slot_width, vent_slot_length)
    .cutBlind(-wall_thickness * 2)
)

with_holes = (
    vented
    .faces(">Z")
    .workplane()
    .rarray(mount_hole_spacing, mount_hole_spacing, 2, 2)
    .hole(mount_hole_diameter)
)

result = (
    with_holes
    .edges("|Z")
    .chamfer(chamfer_size)
)
