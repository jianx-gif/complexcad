import cadquery as cq
import math
# Parameters
num_teeth = 24
module = 2.5
pressure_angle_deg = 20
gear_height = 20.0
hole_diameter = 5.0
counterbore_diameter = 10.0
counterbore_depth = 3.0
chamfer_distance = 0.5
# Derived dimensions
pitch_diameter = module * num_teeth  # 60
pitch_radius = pitch_diameter / 2.0  # 30
addendum = module
dedendum = 1.25 * module
outer_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum
circular_pitch = math.pi * module
tooth_thickness = circular_pitch / 2.0  # at pitch circle
angle_per_tooth = 2 * math.pi / num_teeth
tooth_angle = tooth_thickness / pitch_radius
space_angle = angle_per_tooth - tooth_angle
space_arc_length = space_angle * pitch_radius
# Base gear blank as cylinder with outer radius
gear = cq.Workplane('XY').circle(outer_radius).extrude(gear_height)
# Cut away space between teeth using rectangular blocks
radial_extent = outer_radius - root_radius
for i in range(num_teeth):
    cut = (
        cq.Workplane('XY')
        .rect(radial_extent, space_arc_length)
        .extrude(gear_height)
        .translate(((outer_radius + root_radius) / 2.0, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), math.degrees(i * angle_per_tooth))
    )
    gear = gear.cut(cut)
# Central hub
hub_radius = pitch_radius * 0.4
hub_height = gear_height * 0.8
hub = cq.Workplane('XY').circle(hub_radius).extrude(hub_height)
# Counterbore holes on hub top face
hub = (
    hub.faces('>Z')
    .workplane()
    .polarArray(radius=hub_radius * 0.6, count=4, startAngle=0, angle=360)
    .cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
)
# Combine gear and hub
result = gear.union(hub)
# Apply chamfer to vertical edges of teeth
result = result.edges('|Z').chamfer(chamfer_distance)
