import cadquery as cq
outer_diameter = 80.0
inner_diameter = 50.0
thickness = 70.0
rib_height = 30.0
rib_width = 10.0
rib_thickness = 4.0
rib_count = 6
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius + rib_thickness, thickness)
    .lineTo(inner_radius + rib_thickness, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_thickness, thickness)
    .translate((inner_radius + rib_thickness / 2.0, 0, thickness / 2.0))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .polarArray(radius=inner_radius + rib_thickness / 2.0, count=rib_count, startAngle=0, angle=360)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
result = combined
