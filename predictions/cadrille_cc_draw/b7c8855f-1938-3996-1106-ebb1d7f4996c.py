import cadquery as cq
base_length = 70.0
base_width = 30.0
base_thickness = 5.0
rib_width = 10.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = (
    combined.faces(">Z").workplane()
    .rect(base_length - 2 * rib_spacing, rib_width)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
