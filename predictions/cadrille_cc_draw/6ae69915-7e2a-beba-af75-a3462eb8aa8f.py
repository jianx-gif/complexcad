import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
fillet_radius = 2.0
chamfer_distance = 0.5
mount_hole_dia = 5.0
mount_hole_spacing = 20.0
mount_hole_offset = 10.0
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
combined = base.union(rib)
combined = combined.edges("|Z").fillet(fillet_radius)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(mount_hole_dia)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(mount_hole_dia)
)
result = (
    combined
    .faces(">Z")
    .workplane()
    .hole(mount_hole_dia)
)
