import cadquery as cq
import math
module = 2.0
num_teeth = 32
pressure_angle_deg = 20.0
gear_width = 16.0
bore_diameter = 12.0
set_screw_diameter = 4.0
set_screw_head_diameter = 8.0
set_screw_head_height = 2.0
fillet_radius = 0.5
chamfer_size = 0.3
overlap = 0.2
pitch_diameter = module * num_teeth
addendum = module
dedendum = 1.25 * module
outer_diameter = pitch_diameter + 2 * addendum
root_diameter = pitch_diameter - 2 * dedendum
pressure_angle = math.radians(pressure_angle_deg)
base_diameter = pitch_diameter * math.cos(pressure_angle)
outer_radius = outer_diameter / 2.0
root_radius = root_diameter / 2.0
bore_radius = bore_diameter / 2.0
tooth_radial_height = outer_radius - root_radius
tooth_width = (math.pi * module) / 2.0 * 0.9
blank_profile = (
    cq.Workplane('XZ')
    .moveTo(bore_radius, 0)
    .vLine(gear_width)
    .hLine(root_radius - bore_radius)
    .vLine(-gear_width)
    .close()
)
blank = blank_profile.revolve()
gear = (
    blank
    .faces('>Z')
    .workplane()
    .hole(set_screw_head_diameter, set_screw_head_height)
    .faces('>Z')
    .workplane()
    .hole(set_screw_diameter, gear_width - set_screw_head_height)
)
tooth = (
    cq.Workplane('YZ')
    .rect(gear_width, tooth_width)
    .extrude(tooth_radial_height)
    .translate((root_radius - overlap, 0, 0))
    .fillet(fillet_radius)
)
gear_with_teeth = gear
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    gear_with_teeth = gear_with_teeth.union(tooth.rotate((0, 0, 0), (0, 0, 1), angle))
gear_with_teeth = gear_with_teeth.edges('>Z').chamfer(chamfer_size)
result = gear_with_teeth