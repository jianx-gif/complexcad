import cadquery as cq
import math
outer_diameter = 50.0
inner_diameter = 30.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_count = 6
rib_radius = outer_diameter / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer_cyl = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_cyl)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(outer_cyl)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
    .translate((0, 0, wall_thickness))
)
rib = rib.translate((outer_radius - rib_width / 2.0, 0, wall_thickness))
rib = rib.translate((outer_radius - rib_width / 2.0, 0, wall_thickness))
combined = outer_cyl.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
result = combined
