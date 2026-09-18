import cadquery as cq
import math
gear_thickness = 8.0
gear_thickness = 8.0
num_teeth = 12
tooth_width = 4.0
tooth_height = 6.0
tooth_depth = 2.0
tooth_width = 4.0
tooth_height = 6.0
tooth_width = 6.0
tooth_depth = 2.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(gear_thickness, gear_thickness)
    .extrude(gear_thickness)
)
gear_body = base.shell(-gear_thickness)
gear_body = (
    gear_body
    .faces(">Z")
    .workplane()
    .center(0, gear_thickness/2 - tooth_width/2)
    .rect(tooth_width, tooth_height)
    .cutBlind(-gear_thickness)
)
gear_body = (
    gear_body
    .faces(">Z")
    .workplane()
    .center(0, gear_thickness/2 - tooth_height/2)
    .rect(tooth_width, tooth_height)
    .cutBlind(-gear_thickness)
)
gear_body = (
    gear_body
    .faces(">Z")
    .workplane()
    .center(0, gear_thickness/2 - tooth_height/2)
    .rect(tooth_width, tooth_height)
    .cutBlind(-gear_thickness)
)
result = (
    gear_body
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(tooth_width, tooth_height)
    .cutBlind(-gear_thickness)
)
