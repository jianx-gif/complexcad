import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 12.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
rib = (
    cq.Workplane("XY")
    .center(inner_diameter / 2 + rib_spacing / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = combined.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
