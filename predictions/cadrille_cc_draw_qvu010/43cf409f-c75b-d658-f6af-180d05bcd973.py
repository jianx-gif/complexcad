import cadquery as cq
outer_diameter = 82.0
inner_diameter = 40.0
thickness = 30.0
rib_width = 10.0
rib_height = 20.0
rib_thickness = 5.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 15.0
rib_count = 6
rib_spacing = 12.0
rib_height = 10.0
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
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
)
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
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
    .polarArray(mount_hole_offset, 0, 360, mount_hole_offset)
    .hole(mount_hole_diameter)
)
result = combined
