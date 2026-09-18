import cadquery as cq
import math
outer_radius = 80.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
rib_height = 2.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
rib_count = 6
rib_offset = 5.0
rib_height = 2.0
rib_count = 4
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .close()
)
solid = profile.revolve(360)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges(">Z").chamfer(chamfer_size)
result = solid
