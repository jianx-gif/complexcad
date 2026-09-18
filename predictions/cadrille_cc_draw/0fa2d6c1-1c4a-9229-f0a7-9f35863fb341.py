import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 60.0
rib_height = 40.0
rib_width = 10.0
rib_depth = 8.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
rib_count = 4
rib_offset = 10.0
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
rib = rib.translate((rib_offset, 0, 0))
)
rib = rib.translate((rib_offset, 0, 0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces("<Z").workplane().hole(inner_diameter)
result = combined
