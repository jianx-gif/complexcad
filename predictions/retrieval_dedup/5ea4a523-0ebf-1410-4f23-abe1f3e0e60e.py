import cadquery as cq
arm_length = 70.0
arm_width = 20.0
arm_thickness = 10.0
taper_length = 30.0
taper_width_end = 12.0
round_end_radius = taper_width_end / 2.0
base_length = arm_length - taper_length - 2 * round_end_radius
offset = (arm_width - taper_width_end) / 2.0
p0 = (0.0, 0.0)
p1 = (base_length, 0.0)
p2 = (base_length + taper_length, offset)
mid = (base_length + taper_length + round_end_radius, arm_width / 2.0)
p4 = (base_length + taper_length, arm_width - offset)
p5 = (base_length, arm_width)
p6 = (0.0, arm_width)
arm = (
    cq.Workplane('XY')
    .polyline([p0, p1])
    .lineTo(*p2)
    .threePointArc(mid, p4)
    .lineTo(*p5)
    .lineTo(*p6)
    .close()
    .extrude(arm_thickness)
)
result = arm
