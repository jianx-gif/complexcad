import cadquery as cq
import math
base_diameter = 40.0
base_thickness = 8.0
base_height = 20.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_depth = 12.0
hole_count = 8
hole_circle_radius = base_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(base_diameter / 2.0)
    .extrude(base_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_height - rib_height))
)
base = base.union(rib)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutBlind(-hole_depth)
)
hole_positions = [
    (hole_circle_radius * math.cos(2 * math.pi * i / hole_count),
     hole_circle_radius * math.sin(2 * math.pi * i / hole_count))
]
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = base
