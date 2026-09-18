import cadquery as cq
import math
base_radius = 10.0
base_height = 12.0
wall_thickness = 2.0
inner_radius = 30.0
inner_height = 15.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(inner_radius, inner_height)
    .cutBlind(-wall_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(hole_diameter / 2)
    .cutBlind(-hole_depth)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(hole_diameter / 2)
    .cutBlind(-hole_depth)
)
result = base
