import cadquery as cq
import math
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 5.0
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_count = 6
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
result = combined
