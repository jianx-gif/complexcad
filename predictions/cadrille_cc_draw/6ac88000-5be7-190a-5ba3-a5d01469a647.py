import cadquery as cq
import math
base_radius = 20.0
base_height = 14.0
wall_thickness = 2.0
base_radius = base_radius - wall_thickness
base_thickness = 4.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = base_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(base_radius)
    .extrude(base_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(base_radius)
    .extrude(base_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_radius - 2 * wall_thickness, base_height - 2 * wall_thickness)
    .cutBlind(-base_height)
)
result = base
