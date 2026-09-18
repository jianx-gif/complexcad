import cadquery as cq

arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
base_length = 20.0
base_height = 30.0
pivot_radius = 5.0
hole_diameter = 4.0
hole_depth = 8.0
pocket_width = 12.0
pocket_height = 14.0
pocket_depth = 6.0
fillet_radius = 0.8

arm_solid = cq.Workplane('XY').rect(arm_length, arm_width).extrude(arm_thickness)
base_solid = (
    cq.Workplane('XY')
    .rect(base_length, base_height)
    .translate(((arm_length - base_length/2), (arm_width/2 + (base_height - arm_width)/2)))
    .extrude(arm_thickness)
)
profile = arm_solid.union(base_solid)
result = (
    profile
    .faces('<Z')
    .workplane()
    .center(arm_length/2, arm_width/2)
    .hole(pivot_radius*2, depth=arm_thickness)
)
result = (
    result
    .faces('<Z')
    .workplane()
    .center(arm_length - base_length/2, arm_width/2)
    .rect(pocket_width, pocket_height)
    .cutBlind(pocket_depth)
)
result = (
    result
    .faces('<Z')
    .workplane(offset=-pocket_depth)
    .center(arm_length - base_length/2, arm_width/2)
    .hole(hole_diameter, depth=hole_depth)
)
result = result.edges().fillet(fillet_radius)
