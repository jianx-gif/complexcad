import cadquery as cq

hex_flat_to_flat = 60
hex_height = 80
wall_thickness = 4
central_hole_diameter = 16
mount_hole_diameter = 8
mount_hole_offset = 20
chamfer_distance = 1.5
rib_width = 12
rib_length = 48
rib_height = 6
pocket_depth = 6
pocket_margin = 5

hex_radius = hex_flat_to_flat / (2 * 0.8660254037844386)

base = (
    cq.Workplane("XY")
    .polygon(6, hex_radius * 2)
    .extrude(hex_height)
)

central_hole = (
    base
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
)

mount_holes = (
    central_hole
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_offset, 0), (mount_hole_offset, 0)])
    .hole(mount_hole_diameter)
)

rib = (
    mount_holes
    .faces(">Z")
    .workplane()
    .center(hex_radius - rib_width / 2, 0)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

pocket = (
    rib
    .faces("<Z")
    .workplane()
    .polygon(6, (hex_flat_to_flat - 2 * pocket_margin) / (2 * 0.8660254037844386))
    .cutBlind(-pocket_depth)
)

result = (
    pocket
    .edges("|Z")
    .chamfer(chamfer_distance)
)
