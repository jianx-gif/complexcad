import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 20.0
thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_depth = 10.0
hole_spacing = 15.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2 - rib_thickness / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
combined = base.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
]
for x, y in hole_positions:
    combined = (
        combined
        .faces(">Z")
        .workplane()
        .pushPoints(hole_positions)
        .hole(hole_diameter)
    )
rib = (
    cq.Workplane("XY")
    .center(x, y)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.union(rib)
result = combined
