import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
    .translate((0, 0, base))
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
    .translate((0, 0, base))
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
