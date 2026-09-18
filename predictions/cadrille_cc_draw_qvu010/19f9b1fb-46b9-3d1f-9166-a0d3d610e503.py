import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 12.0
rib_height = 5.0
rib_width = 6.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
rib_count = 8
rib_width = 12.0
rib_height = 8.0
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
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=mount_hole_offset, count=rib_count, startAngle=0, angle=360).hole(mount_hole_diameter)
result = combined
