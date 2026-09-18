import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 20.0
rib_count = 4
rib_count = 3
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(rib_spacing, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((rib_spacing, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
result = combined
