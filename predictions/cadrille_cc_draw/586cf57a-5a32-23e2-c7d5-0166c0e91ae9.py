import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 15.0
rib_height = 10.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
rib_margin = 5.0
chamfer_size = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 20.0
rib_count = 4
rib_spacing = 20.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(rib_width / 2)
    .extrude(rib_height)
    .translate((0, 0, thickness))
)
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness + rib_height))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = (
    combined.faces(">Z").workplane()
    .polarArray(radius=outer_diameter / 2 - rib_margin, startAngle=0, angle=360, count=rib_count)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
