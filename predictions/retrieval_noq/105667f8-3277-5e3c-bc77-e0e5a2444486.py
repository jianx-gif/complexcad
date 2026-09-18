import cadquery as cq

plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
slot_length = 40.0
slot_width = 12.0
slot_fillet_radius = 3.0
hole_diameter = 6.0
hole_offset_from_slot = 10.0
hole_depth = plate_thickness - 2.0
corner_chamfer = 2.0
rib_height = 4.0
rib_width = 6.0
rib_length = plate_length - 20.0
mount_hole_dia = 5.0
mount_offset = 10.0

# Base plate
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
# Central slot cut through
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutThruAll()
)
# Fillet slot ends (vertical edges)
result = (
    result
    .edges("|Z")
    .fillet(slot_fillet_radius)
)
# Blind holes adjacent to slot
hole_offset = slot_width / 2 + hole_offset_from_slot
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_offset, 0)
    .hole(hole_diameter, depth=hole_depth)
    .center(-2 * hole_offset, 0)  # move to opposite side
    .hole(hole_diameter, depth=hole_depth)
)
# Mounting holes near corners
corner_x = plate_length / 2 - mount_offset
corner_y = plate_width / 2 - mount_offset
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (corner_x, corner_y),
        (corner_x, -corner_y),
        (-corner_x, corner_y),
        (-corner_x, -corner_y),
    ])
    .hole(mount_hole_dia)
)
# Stiffening ribs on top surface
rib_y_positions = [plate_width / 4, -plate_width / 4]
for y in rib_y_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(0, y)
        .rect(rib_width, rib_length)
        .extrude(rib_height)
    )
# Chamfer outer edges
result = (
    result
    .edges("|Z")
    .chamfer(corner_chamfer)
)
