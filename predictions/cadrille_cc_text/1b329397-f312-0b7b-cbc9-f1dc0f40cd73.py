import cadquery as cq
base_radius = 30.0
gear_height = 10.0
tooth_width = 4.0
tooth_depth = 5.0
key_width = 8.0
key_depth = 5.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(base_radius).extrude(gear_height)
tooth = (
    cq.Workplane('XY')
    .rect(tooth_width, tooth_depth)
    .extrude(gear_height)
    .translate((0, 0, gear_height))
)
gear_body = base.union(tooth)
key = (
    cq.Workplane('XY')
    .center(base_radius - key_depth/2, 0)
    .rect(key_width, key_depth)
    .extrude(key_depth)
    .translate((0, 0, gear_height))
)
gear_body = gear_body.union(key)
gear_body = (
    gear_body
    .faces('>Z')
    .workplane()
    .center(base_radius - key_depth/2, 0)
    .rect(key_width, key_depth)
    .cutBlind(key_depth)
)
result = gear_body
