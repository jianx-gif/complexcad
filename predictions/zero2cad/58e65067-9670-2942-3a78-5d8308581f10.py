import cadquery as cq

# Parameters
outer_radius = 40.0
wall_thickness = 3.0
height = 60.0
boss_radius = 12.0
boss_height = 10.0
vent_hole_diameter = 2.0
vent_rows = 4
vent_cols = 6
vent_spacing = 8.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
chamfer_size = 1.0
slot_width = 6.0
slot_height = 12.0
slot_depth = 8.0

# Base solid: revolve a composite profile
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(0, height)
    .close()
)
solid = profile.revolve()

# Shell to create thin-walled housing
hollow = solid.shell(wall_thickness)

# Add central boss on top face
with_boss = (
    hollow
    .faces(">Z")
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
)

# Add side slot for cable entry (cut through wall)
slot = (
    with_boss
    .faces(">X")
    .workplane()
    .center(0, height/2)
    .rect(slot_width, slot_height)
    .cutBlind(-slot_depth)
)

# Chamfer outer vertical edges
chamfered = slot.edges("|Z").chamfer(chamfer_size)

# Vent holes pattern on top face (through wall)
vented = (
    chamfered
    .faces(">Z")
    .workplane()
    .rarray(vent_spacing, vent_spacing, vent_cols, vent_rows)
    .hole(vent_hole_diameter)
)

# Mounting holes on top face (four corners)
mount_points = [
    (mount_hole_offset, mount_hole_offset),
    (-mount_hole_offset, mount_hole_offset),
    (mount_hole_offset, -mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
]
result = (
    vented
    .faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)
