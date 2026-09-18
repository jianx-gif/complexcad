import cadquery as cq
import math
gear_outer_radius = 30.0
gear_inner_radius = 12.0
gear_height = 8.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_depth = 6.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(gear_outer_radius, gear_outer_radius)
    .extrude(gear_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(gear_outer_radius, gear_outer_radius)
    .cutBlind(-gear_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(gear_inner_radius * 2, gear_outer_radius * 2)
    .cutBlind(-gear_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(gear_inner_radius * 2, gear_outer_radius * 2)
    .cutBlind(-gear_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(hole_offset, 0)
    .hole(hole_diameter)
)
result = base
