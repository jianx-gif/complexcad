import cadquery as cq
import math
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
arm_height = 12.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 3
hole_cols = 3
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, arm_length)
    .extrude(rib_height)
    .translate((arm_length/2 - rib_width/2, 0, 0))
)
rib = rib.translate((arm_length/2 - rib_width/2, 0, 0))
combined = base.union(rib)
hole_positions = [
    (arm_length/2 - hole_spacing, 0),
    (arm_length/2 - hole_spacing, 0),
    (arm_length/2 - hole_spacing, 0),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
