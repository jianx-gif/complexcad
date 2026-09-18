import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 12.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius - rib_thickness)
    .extrude(wall_thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius - rib_thickness)
    .extrude(wall_thickness + rib_height)
    .translate((0, 0, wall_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
