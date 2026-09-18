import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 15.0
rib_height = 5.0
rib_width = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_spacing = 12.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (outer_diameter / 2, 0),
        (outer_diameter / 2, thickness),
        (outer_diameter / 2, thickness),
        (inner_diameter / 2, thickness),
        (inner_diameter / 2, 0)
    ])
    .close()
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
result = combined
