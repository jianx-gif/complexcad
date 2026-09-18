import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_radius = outer_diameter / 2.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0 - rib_radius, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(inner_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(inner_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(inner_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(inner_diameter)
result = combined
