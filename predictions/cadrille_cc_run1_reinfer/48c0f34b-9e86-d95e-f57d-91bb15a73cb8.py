import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 10.0
rib_width = 5.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
mount_hole_offset = 15.0
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
rib = rib.union(rib)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .circle(inner_diameter / 2)
    .extrude(thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
mount_points = [
    (-mount_hole_offset, 0),
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)
