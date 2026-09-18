import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 6.0
rib_width = 30.0
rib_height = 12.0
hole_diameter = 10.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
pocket_depth = 2.0
pocket_margin = 5.0

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

rib = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness)
    .rect(rib_width, plate_width)
    .extrude(rib_height)
)

combined = base.union(rib)

through_hole = (
    cq.Workplane("XY")
    .circle(hole_diameter / 2)
    .extrude(plate_thickness + rib_height)
)

combined = combined.cut(through_hole)

mount_hole_positions = [
    (mount_hole_offset, mount_hole_offset),
    (plate_length - mount_hole_offset, mount_hole_offset),
    (mount_hole_offset, plate_width - mount_hole_offset),
    (plate_length - mount_hole_offset, plate_width - mount_hole_offset),
]

mount_holes = (
    cq.Workplane("XY")
    .pushPoints(mount_hole_positions)
    .circle(mount_hole_diameter / 2)
    .extrude(plate_thickness + rib_height)
)

combined = combined.cut(mount_holes)

pocket = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * pocket_margin, plate_width - 2 * pocket_margin)
    .extrude(-pocket_depth)
)

combined = combined.cut(pocket)

result = combined.edges("|Z").chamfer(chamfer_size)
