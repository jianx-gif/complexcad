import cadquery as cq
import math
outer_radius = 45.0
inner_radius = 10.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(outer_radius, outer_radius)
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius - rib_width / 2, 0, 0))
combined = base.union(rib)
combined = combined.faces(">Z").edges().chamfer(chamfer_distance)
combined = combined.faces(">Z").edges().chamfer(chamfer_distance)
result = combined
