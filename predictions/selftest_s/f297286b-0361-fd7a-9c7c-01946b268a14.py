import cadquery as cq
import math
# Parameters
module = 2.0
num_teeth = 26
helix_angle_deg = 20.0
gear_width = 10.0
pressure_angle_deg = 20.0
clearance = 0.2
chamfer_size = 0.5
# Derived dimensions
pitch_diameter = module * num_teeth
pitch_radius = pitch_diameter / 2.0
circular_pitch = math.pi * module
addendum = module
dedendum = 1.25 * module + clearance
outer_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum
base_radius = pitch_radius * math.cos(math.radians(pressure_angle_deg))
# Tooth geometry
tooth_thickness = circular_pitch / 2.0
# Helix calculations
helix_angle_rad = math.radians(helix_angle_deg)
lead = (math.pi * pitch_diameter) / math.tan(helix_angle_rad)
# total twist over gear width
twist_angle = (gear_width / lead) * 360.0
# Central flange
flange_radius = root_radius * 0.6
flange_thickness = gear_width * 0.4
# Base gear blank (cylinder) and flange union
gear_blank = (
    cq.Workplane("XY")
    .cylinder(gear_width, outer_radius * 2)
    .union(
        cq.Workplane("XY")
        .cylinder(flange_thickness, flange_radius * 2)
        .translate((0, 0, (gear_width - flange_thickness) / 2))
    )
)
# Single tooth solid for cutting (helical)
tooth_profile = (
    cq.Workplane("XY")
    .moveTo(root_radius, -tooth_thickness / 2)
    .lineTo(outer_radius, -tooth_thickness / 2)
    .lineTo(outer_radius, tooth_thickness / 2)
    .lineTo(root_radius, tooth_thickness / 2)
    .close()
    .twistExtrude(gear_width, twist_angle)
)
# Cut teeth around the gear
gear = gear_blank
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    rotated_tooth = tooth_profile.rotate((0, 0, 0), (0, 0, 1), angle)
    gear = gear.cut(rotated_tooth)
# Chamfer outer edges for safety
result = gear.edges().chamfer(chamfer_size)