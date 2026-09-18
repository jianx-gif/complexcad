import cadquery as cq
import math
num_teeth = 23
module = 2.0
gear_thickness = 8.0
outer_radius = module * (num_teeth + 2) / 2.0
web_thickness = 2.0
hub_base_radius = 8.0
bore_diameter = 6.0
bore_radius = bore_diameter / 2.0
key_width = 2.0
key_depth = hub_base_radius - bore_radius
# Base thin-walled cylinder
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(gear_thickness)
thin_body = outer_cyl.shell(web_thickness)
# Hub overlapping thin wall for continuity
hub = cq.Workplane('XY').circle(hub_base_radius + web_thickness/2).extrude(gear_thickness)
gear = thin_body.union(hub)
# Central bore
gear = gear.cut(cq.Workplane('XY').circle(bore_radius).extrude(gear_thickness))
# Tooth space cuts
tooth_angle = 360.0 / num_teeth
space_angle = tooth_angle * 0.5
radius_mid = (hub_base_radius + web_thickness + outer_radius) / 2.0
space_width = 2 * radius_mid * math.tan(math.radians(space_angle / 2.0))
radial_depth = outer_radius - (hub_base_radius + web_thickness)
for i in range(num_teeth):
    angle = i * tooth_angle
    cut_shape = (
        cq.Workplane('XY')
        .center(radius_mid, 0)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .rect(space_width, radial_depth)
        .extrude(gear_thickness)
    )
    gear = gear.cut(cut_shape)
# Keyway slot
keyway = (
    cq.Workplane('XY')
    .box(key_depth, key_width, gear_thickness)
    .translate((hub_base_radius - key_depth/2.0, 0, 0))
)
gear = gear.cut(keyway)
result = gear