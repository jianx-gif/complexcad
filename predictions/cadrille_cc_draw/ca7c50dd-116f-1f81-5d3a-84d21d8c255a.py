import cadquery as cq
outer_width = 80.0
outer_height = 50.0
outer_height = 8.0
wall_thickness = 8.0
rib_width = 12.0
rib_height = 6.0
rib_spacing = 15.0
rib_count = 6
rib_count = 8
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(outer_width - 2 * wall_thickness, outer_height - 2 * wall_thickness)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(outer_height)
    .translate((0, outer_height / 2 + rib_spacing / 2, 0))
)
rib = rib.translate((0, outer_height / 2 + rib_spacing / 2, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().hole(rib_width)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
