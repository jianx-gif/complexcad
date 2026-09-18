import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 20.0
rib_width = 10.0
rib_height = 12.0
rib_thickness = 4.0
rib_count = 6
mount_hole_diameter = 5.0
mount_hole_offset = 15.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((outer_radius - rib_thickness / 2.0, 0, 0))
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
    .center(0, 0)
    .circle(mount_hole_diameter / 2.0)
    .cutBlind(-thickness)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
