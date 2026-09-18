import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
pocket_length = 40.0
pocket_width = 30.0
pocket_depth = 4.0
chamfer_size = 1.0
mount_hole_dia = 5.0
hole_offset = 12.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_width, plate_width - 2 * rib_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (plate_length/2 - mount_hole_offset, plate_width/2 - mount_hole_offset),
    (-plate_length/2 + mount_hole_offset, plate_width/2 - mount_hole_offset),
    (plate_length/2 - mount_hole_offset, -plate_width/2 + mount_hole_offset),
    (-plate_length/2 + mount_hole_offset, -plate_width/2 + mount_hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_dia)
)
base = base.edges("|Z").chamfer(chamfer_size)
result = base
