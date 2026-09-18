import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 4.0
rib_width = 6.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_depth = thickness / 2.0
hole_count = 6
hole_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0 - rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness / 2.0))
combined = base.union(rib)
hole_positions = [
    (hole_radius * math.cos(2 * math.pi * i / hole_count),
     hole_radius * math.sin(2 * math.pi * i / hole_count))
    for i in range(hole_count)
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
