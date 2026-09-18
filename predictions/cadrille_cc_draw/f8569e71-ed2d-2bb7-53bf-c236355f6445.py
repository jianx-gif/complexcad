import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 12.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
rib_count = int(outer_diameter / rib_spacing)
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
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
result = combined
