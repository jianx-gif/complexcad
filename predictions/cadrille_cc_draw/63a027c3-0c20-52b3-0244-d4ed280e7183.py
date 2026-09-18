import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
rib_count = 4
rib_count = 6
rib_radius = outer_diameter / 2.0
rib_height = thickness * 0.6
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(rib_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(rib_radius)
    .extrude(thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = (
    combined.faces(">Z")
    .workplane()
    .polarArray(radius=outer_diameter / 2.0, startAngle=0, angle=360, count=rib_count)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
