import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 30.0
rib_height = 5.0
rib_width = 10.0
rib_thickness = 4.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_count = 6
rib_spacing = 12.0
rib_height = 10.0
rib_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = (
    combined.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
