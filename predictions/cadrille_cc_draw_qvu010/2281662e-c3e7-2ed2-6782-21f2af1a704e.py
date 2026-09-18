import cadquery as cq
import math
outer_diameter = 100.0
inner_diameter = 30.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 12
chamfer_size = 0.5
hole_diameter = 5.0
hole_depth = thickness * 0.6
hole_count = 6
hole_radius = outer_diameter / 2.0
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
    (hole_radius * math.cos(math.radians(i * 36)),
    (hole_radius * math.sin(math.radians(i * 36)),
    (hole_radius * math.sin(math.radians(i * 36)),
    (hole_radius * math.sin(math.radians(i * 36)),
]
for x, y in hole_positions:
    combined = (
        combined
        .faces(">Z")
        .workplane()
        .pushPoints(hole_positions)
        .hole(hole_diameter)
    )
result = combined
