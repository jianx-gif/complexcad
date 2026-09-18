import cadquery as cq
outer_width = 80.0
outer_height = 60.0
outer_height = 20.0
wall_thickness = 4.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_spacing = 15.0
chamfer_size = 1.0
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
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
result = combined
