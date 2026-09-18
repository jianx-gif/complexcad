import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 20.0
rib_height = 10.0
rib_width = 8.0
rib_thickness = 4.0
rib_count = 6
rib_count = 8
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_offset = 10.0
rib_height = 5.0
rib_count = 4
rib_offset = 15.0
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
rib = rib.translate((rib_offset, 0, rib_height / 2))
)
rib = rib.translate((rib_offset, 0, rib_height / 2))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
result = combined
