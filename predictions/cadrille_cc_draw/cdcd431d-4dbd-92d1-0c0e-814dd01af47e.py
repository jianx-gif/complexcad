import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 12.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 10.0
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
rib = rib.translate((rib_spacing, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(hole_diameter)
result = combined
