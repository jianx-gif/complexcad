import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
cutout_diameter = 30.0
rib_width = 30.0
rib_height = 6.0
hole_diameter = 5.0
hole_depth = 4.0
hole_offset = 12.0
mount_hole_diameter = 6.0
mount_hole_offset = 10.0
chamfer_size = 1.0

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

base = (
    base.faces(">Z")
    .workplane()
    .circle(cutout_diameter / 2)
    .cutBlind(-plate_thickness)
)

rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)

rib = (
    rib.faces(">Z")
    .workplane()
    .pushPoints([
        (hole_offset, 0),
        (-hole_offset, 0),
        (0, hole_offset),
        (0, -hole_offset),
    ])
    .hole(hole_diameter, depth=hole_depth)
)

mount_points = [
    (plate_length / 2 - mount_hole_offset, plate_width / 2 - mount_hole_offset),
    (-plate_length / 2 + mount_hole_offset, plate_width / 2 - mount_hole_offset),
    (-plate_length / 2 + mount_hole_offset, -plate_width / 2 + mount_hole_offset),
    (plate_length / 2 - mount_hole_offset, -plate_width / 2 + mount_hole_offset),
]

rib = (
    rib.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

result = rib.edges("|Z").chamfer(chamfer_size)
