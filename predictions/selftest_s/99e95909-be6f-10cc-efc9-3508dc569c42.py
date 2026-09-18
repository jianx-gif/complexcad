import cadquery as cq

base_width = 80.0
base_depth = 40.0
base_height = 5.0
base_corner_radius = 3.0
rib_width = 4.0
rib_height = 2.0
rib_spacing = 10.0
pilot_hole_diameter = 3.0
clip_wall = 2.0
clip_height = 12.0
clip_arm_length = 30.0
clip_flex_radius = 8.0
chamfer_size = 1.0
fillet_radius = 0.8

result = (
    cq.Workplane('XY')
    .rect(base_width, base_depth)
    .extrude(base_height)
    .edges('|Z')
    .fillet(base_corner_radius)
    .faces('>Z')
    .workplane()
    .tag('base_top_wp')
)

rib_count = int((base_width - 2 * base_corner_radius) // rib_spacing)
result = (
    result
    .workplaneFromTagged('base_top_wp')
    .pushPoints([
        (-base_width/2 + base_corner_radius + rib_spacing/2 + i * rib_spacing, 0)
        for i in range(rib_count)
    ])
    .rect(rib_width, rib_height)
    .extrude(3.0)
    .edges('>Z')
    .fillet(fillet_radius)
)

result = (
    result
    .workplaneFromTagged('base_top_wp')
    .center(0, 0)
    .circle(pilot_hole_diameter / 2)
    .cutBlind(base_height + 5.0)
)

path = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(clip_arm_length / 2, 0)
    .threePointArc((clip_arm_length / 2, clip_flex_radius / 2), (clip_arm_length, clip_flex_radius))
    .wire()
)

clip_solid = (
    cq.Workplane('XZ')
    .center(base_width / 2, 0)
    .rect(clip_wall, clip_height)
    .sweep(path)
)

result = result.union(clip_solid)

result = (
    result
    .edges('>X')
    .chamfer(chamfer_size)
)
