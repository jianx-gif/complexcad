import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_extension = 10.0
pocket_length = 40.0
pocket_width = 30.0
pocket_depth = 4.0
chamfer_size = 1.0
mount_hole_dia = 5.0
hole_offset = 12.0

base_plate = cq.Workplane("XY").rect(plate_length, plate_width).extrude(plate_thickness)

rib1 = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_extension, rib_width)
    .extrude(-rib_height)
    .translate((0, plate_width / 2 - rib_width / 2 - rib_extension, 0))
)

rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width - 2 * rib_extension)
    .extrude(-rib_height)
    .translate((plate_length / 2 - rib_width / 2 - rib_extension, 0, 0))
)

plate_with_ribs = base_plate.union(rib1).union(rib2)

pocket_body = (
    cq.Workplane("XY")
    .rect(pocket_length, pocket_width)
    .extrude(pocket_depth)
    .translate((0, 0, plate_thickness - pocket_depth))
)

pocket_chamfered = pocket_body.edges("|Z").chamfer(chamfer_size)

result = plate_with_ribs.cut(pocket_chamfered)

hole_positions = [
    (-plate_length / 2 + hole_offset, -plate_width / 2 + hole_offset),
    (plate_length / 2 - hole_offset, -plate_width / 2 + hole_offset),
    (-plate_length / 2 + hole_offset, plate_width / 2 - hole_offset),
    (plate_length / 2 - hole_offset, plate_width / 2 - hole_offset),
]

result = result.faces(">Z").workplane().pushPoints(hole_positions).hole(mount_hole_dia)
