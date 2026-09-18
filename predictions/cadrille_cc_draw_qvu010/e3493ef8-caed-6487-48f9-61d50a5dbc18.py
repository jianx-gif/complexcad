import cadquery as cq
outer_width = 80.0
outer_height = 60.0
outer_height = 40.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 15.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, outer_height - rib_height))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_width)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_width)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
