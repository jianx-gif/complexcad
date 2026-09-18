import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 60.0
rib_height = 12.0
rib_width = 10.0
rib_depth = 8.0
rib_count = 6
mount_hole_diameter = 5.0
mount_hole_offset = 20.0
chamfer_size = 1.0
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
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_depth, thickness)
    .translate((outer_radius - rib_depth / 2.0, 0, thickness / 2.0))
)
combined = combined.union(rib)
result = combined
