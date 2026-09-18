import cadquery as cq
import math

number_of_teeth = 42
module = 2.0
pressure_angle_deg = 20.0
gear_thickness = 12.0
bore_diameter = 12.0
oil_drain_diameter = 6.0
oil_drain_offset_factor = 0.7

pitch_diameter = number_of_teeth * module
addendum = module
dedendum = 1.25 * module
outer_diameter = pitch_diameter + 2 * addendum
root_diameter = pitch_diameter - 2 * dedendum
outer_radius = outer_diameter / 2.0
root_radius = root_diameter / 2.0
circular_pitch = math.pi * module
tooth_thickness = circular_pitch / 2.0
tooth_half_width = tooth_thickness / 2.0
angle_step = 360.0 / number_of_teeth
oil_drain_offset = outer_radius * oil_drain_offset_factor

teeth = []
for i in range(number_of_teeth):
    angle = i * angle_step
    tooth_profile = (
        cq.Workplane("XZ")
        .moveTo(root_radius, -tooth_half_width)
        .lineTo(outer_radius, -tooth_half_width)
        .lineTo(outer_radius, tooth_half_width)
        .lineTo(root_radius, tooth_half_width)
        .close()
        .extrude(gear_thickness)
    )
    rotated_tooth = tooth_profile.rotate((0, 0, 0), (0, 0, 1), angle)
    teeth.append(rotated_tooth)

gear_body = teeth[0]
for solid in teeth[1:]:
    gear_body = gear_body.union(solid)

bore_cut = cq.Workplane("XY").cylinder(gear_thickness + 2.0, bore_diameter / 2.0)
gear_body = gear_body.cut(bore_cut)

oil_drain_cut = (
    cq.Workplane("XY")
    .center(oil_drain_offset, 0)
    .cylinder(gear_thickness + 2.0, oil_drain_diameter / 2.0)
)
gear_body = gear_body.cut(oil_drain_cut)

result = gear_body