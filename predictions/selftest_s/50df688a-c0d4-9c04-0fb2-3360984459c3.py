import cadquery as cq

# Parameters
outer_radius = 45
block_height = 30
bore_radius = 10
outer_fillet_radius = 3
mount_hole_diameter = 6
mount_hole_radius = outer_radius - 8
mount_hole_count = 6
step_height = 5
step_thickness = 5
slot_width = 8
slot_length = 20
slot_depth = 5
slot_count = 4
slot_radius = outer_radius - 10

# Base profile for revolve (non‑trivial closed shape)
profile = (
    cq.Workplane("XZ")
    .moveTo(bore_radius, 0)
    .lineTo(bore_radius, block_height)
    .lineTo(outer_radius, block_height)
    .lineTo(outer_radius, step_height)
    .lineTo(bore_radius + step_thickness, step_height)
    .lineTo(bore_radius + step_thickness, 0)
    .close()
)

# Revolve and add features
result = (
    profile.revolve()
    .edges()
    .fillet(outer_fillet_radius)
    .faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_diameter)
    .faces(">Z")
    .workplane()
    .polarArray(radius=slot_radius, count=slot_count, startAngle=0, angle=360)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
