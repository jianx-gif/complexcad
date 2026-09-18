import cadquery as cq
import math

# Parameters
length = 80.0
start_diameter = 15.0
end_major = 25.0
end_minor = 12.0
wall_thickness = 2.0
vent_width = 8.0
vent_height = 3.0
chamfer_distance = 0.5
mount_hole_diameter = 5.0
slot_width = 1.5
slot_angles = [0, 60, 120, 180, 240, 300]

# Base lofted bellows shell (circle to oval)
outer = (
    cq.Workplane('XY')
    .circle(start_diameter / 2)
    .workplane(offset=length)
    .ellipse(end_major / 2, end_minor / 2)
    .loft(combine=True)
)

# Hollow it to desired wall thickness
hollow = outer.shell(-wall_thickness)

# Add circumferential stiffening slots cut through the wall
average_outer_radius = (start_diameter / 2 + max(end_major, end_minor) / 2) / 2
for angle in slot_angles:
    slot = (
        cq.Workplane('XY')
        .box(slot_width, wall_thickness + 0.2, length)
        .translate((average_outer_radius, 0, length / 2))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    hollow = hollow.cut(slot)

# Vent slot on the +X side (through opening)
average_diameter = (start_diameter + max(end_major, end_minor)) / 2
slot_center_x = average_diameter / 2 + vent_width / 2
vent_slot = (
    cq.Workplane('XY')
    .box(vent_width, vent_height, length + 2)
    .translate((slot_center_x, 0, length / 2))
)

vented = hollow.cut(vent_slot)

# Mounting through holes on each end
with_holes = (
    vented.faces('>Z')
    .workplane()
    .hole(mount_hole_diameter)
    .faces('<Z')
    .workplane()
    .hole(mount_hole_diameter)
)

# Chamfer the outer rim edges on both ends for safety
chamfered = (
    with_holes.faces('>Z').edges().chamfer(chamfer_distance)
    .faces('<Z').edges().chamfer(chamfer_distance)
)

result = chamfered
