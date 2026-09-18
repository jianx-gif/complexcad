import cadquery as cq
import math
base_radius = 8.0
base_height = 10.0
base_thickness = 4.0
rib_height = 3.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
