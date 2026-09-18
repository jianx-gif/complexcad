import cadquery as cq
import math

num_teeth = 50
module = 2.0
pressure_angle = math.radians(20)
gear_thickness = 15.0
hub_diameter = 30.0
hub_thickness = 12.0
counterbore_diameter = 10.0
counterbore_depth = 5.0
chamfer_size = 0.5
helix_angle = math.radians(15)

pitch_diameter = module * num_teeth
pitch_radius = pitch_diameter / 2.0
addendum = module
dedendum = 1.25 * module
outer_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum
circular_pitch = math.pi * module
tooth_thickness = circular_pitch / 2.0
height = outer_radius - root_radius
tooth_angle = 360.0 / num_teeth
lead = math.pi * pitch_diameter * math.tan(helix_angle)
axial_pitch = lead / num_teeth

gear = cq.Workplane('XY').circle(outer_radius).extrude(gear_thickness)
gear = gear.faces('>Z').workplane().hole(hub_diameter)
gear = gear.faces('>Z').workplane().hole(counterbore_diameter, counterbore_depth)

cutter = (
    cq.Workplane('XY')
    .center(root_radius + height / 2.0, 0)
    .rect(tooth_thickness, height)
    .extrude(gear_thickness + 2.0)
)

for i in range(num_teeth):
    angle = i * tooth_angle
    z_offset = i * axial_pitch
    tooth = cutter.rotate((0, 0, 0), (0, 0, 1), angle).translate((0, 0, -z_offset))
    gear = gear.cut(tooth)

gear = gear.edges('|Z').chamfer(chamfer_size)

result = gear