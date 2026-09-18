import cadquery as cq
import math
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
base_thickness = 2.0
base_height = 10.0
fillet_radius = 1.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_count = 4
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_thickness)
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
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
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
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
result = (
    base
    .edges("|Z")
    .chamfer(chamfer_distance)
)
