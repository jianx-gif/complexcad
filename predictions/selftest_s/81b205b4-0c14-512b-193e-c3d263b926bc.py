import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 80.0
plate_thickness = 5.0

boss_base_radius = 12.0
boss_top_radius = 10.0
boss_height = 12.0

slot_length = 30.0
slot_width = 6.0
slot_offset_from_center = 20.0

corner_hole_diameter = 5.0
corner_hole_offset = 10.0

edge_chamfer = 1.0

# Base plate with chamfered outer edges
base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges()
    .chamfer(edge_chamfer)
)

# Central tapered boss (revolve)
boss_profile = (
    cq.Workplane("XZ", origin=(0, 0, plate_thickness))
    .moveTo(boss_base_radius, 0)
    .lineTo(boss_base_radius, boss_height)
    .lineTo(boss_top_radius, boss_height)
    .lineTo(boss_top_radius, 0)
    .close()
    .revolve(axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
)

spacer = base_plate.union(boss_profile)

# Slots on each edge
slot = (
    cq.Workplane("XY")
    .center(0, plate_width / 2 - slot_offset_from_center)
    .rect(slot_width, slot_length)
    .extrude(plate_thickness + 1)
)
slots = (
    cq.Workplane("XY")
    .union(slot)
    .union(slot.rotate((0, 0, 0), (0, 0, 1), 90))
    .union(slot.rotate((0, 0, 0), (0, 0, 1), 180))
    .union(slot.rotate((0, 0, 0), (0, 0, 1), 270))
)
spacer = spacer.cut(slots)

# Corner mounting holes on top face
spacer = (
    spacer
    .faces("<Z")
    .workplane()
    .pushPoints([
        (corner_hole_offset, corner_hole_offset),
        (-corner_hole_offset, corner_hole_offset),
        (-corner_hole_offset, -corner_hole_offset),
        (corner_hole_offset, -corner_hole_offset),
    ])
    .hole(corner_hole_diameter)
)

result = spacer
