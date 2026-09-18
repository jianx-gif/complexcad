import cadquery as cq

base_radius = 30.0
gear_height = 10.0
tooth_radial = 5.0
tooth_width = 4.0
num_teeth = 12
key_width = 8.0
key_depth = 5.0
chamfer_size = 0.5

base_disc = cq.Workplane('XY').circle(base_radius).extrude(gear_height)

teeth = (
    cq.Workplane('XY')
    .polarArray(base_radius, count=num_teeth, startAngle=0, angle=360)
    .rect(tooth_width, tooth_radial)
    .extrude(gear_height)
)

gear = base_disc.union(teeth).edges('|Z').chamfer(chamfer_size)

gear_plus = (
    gear
    .faces('>X')
    .workplane()
    .center(0, 0)
    .rect(key_width, gear_height)
    .cutBlind(-key_depth)
)

result = (
    gear_plus
    .faces('<X')
    .workplane()
    .center(0, 0)
    .rect(key_width, gear_height)
    .cutBlind(-key_depth)
)
