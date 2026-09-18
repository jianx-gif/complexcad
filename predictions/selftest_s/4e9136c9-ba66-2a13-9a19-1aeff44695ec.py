import cadquery as cq
import math

# Parameters
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
outer_rim_thickness = 6.0
spacer_height = 20.0
inner_step1_diameter = 40.0
inner_step1_radius = inner_step1_diameter / 2.0
inner_step2_diameter = 30.0
inner_step2_radius = inner_step2_diameter / 2.0
step1_height = 12.0
step2_height = spacer_height - step1_height
central_hole_diameter = 10.0
countersink_diameter = 6.0
countersink_angle = 82.0
countersink_depth = (countersink_diameter / 2.0) / math.tan(math.radians(countersink_angle / 2.0))
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
slot_width = 4.0
slot_length = 12.0

# 2D profile for revolve using Workplane
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, outer_rim_thickness)
    .lineTo(inner_step1_radius, outer_rim_thickness)
    .lineTo(inner_step1_radius, step1_height)
    .lineTo(inner_step2_radius, step1_height)
    .lineTo(inner_step2_radius, spacer_height)
    .lineTo(outer_radius, spacer_height)
    .lineTo(outer_radius, 0)
    .close()
)

result = (
    profile
    .revolve()
    .faces("<Z")
    .hole(central_hole_diameter)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (mount_hole_spacing/2, 0),
        (-mount_hole_spacing/2, 0),
        (0, mount_hole_spacing/2),
        (0, -mount_hole_spacing/2)
    ])
    .cskHole(mount_hole_diameter, countersink_depth, countersink_angle)
    .faces(">Z")
    .workplane()
    .rect(slot_length, slot_width)
    .cutBlind(outer_rim_thickness)
)
