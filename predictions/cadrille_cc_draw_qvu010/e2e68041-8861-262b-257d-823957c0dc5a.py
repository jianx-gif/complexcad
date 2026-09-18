import cadquery as cq
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
thickness = 12.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_spacing = 15.0
rib_spacing = 12.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(outer_diameter, outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = (
    base
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
result = combined
