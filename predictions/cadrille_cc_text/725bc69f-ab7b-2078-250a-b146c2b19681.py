import cadquery as cq
import math
module = 2.0
num_teeth = 20
gear_thickness = 10.0
helix_angle_deg = 15.0
chamfer_size = 0.5
tooth_width = module * num_teeth
tooth_height = module * module
tooth_angle_rad = math.radians(helix_angle_deg)
tooth_width = module * 0.8
tooth_height = module * 0.2
tooth_thickness = gear_thickness * 0.6
tooth_angle_rad = math.radians(helix_angle_deg)
tooth_width = 0.5 * module * math.tan(helix_angle_rad)
tooth_height = 0.5 * module * math.tan(helix_angle_rad)
base = (
    cq.Workplane("XY")
    .rect(tooth_width, tooth_height)
    .extrude(gear_thickness)
)
base = base.edges().chamfer(chamfer_size)
base = base.edges().chamfer(chamfer_size)
base = (
    base.faces(">Z")
    .workplane()
    .hole(tooth_width)
)
base = (
    base.faces(">Z")
    .workplane()
    .hole(tooth_angle_rad)
)
base = (
    base.faces(">Z")
    .workplane()
    .hole(tooth_width)
)
base = (
    base.faces(">Z")
    .workplane()
    .hole(tooth_width)
)
base = (
    base.faces("<Z")
    .workplane()
    .rect(tooth_width, tooth_height)
    .cutBlind(-tooth_height)
)
result = base
