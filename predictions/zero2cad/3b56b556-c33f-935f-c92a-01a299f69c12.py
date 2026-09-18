import cadquery as cq

block_length = 80.0
block_width = 50.0
block_height = 20.0
pocket_length = 60.0
pocket_width = 30.0
pocket_depth = 12.0
fillet_radius = 3.0
chamfer_distance = 1.0
hole_diameter = 8.0
mount_hole_diameter = 5.0
mount_hole_spacing = 40.0
rib_thickness = 4.0
rib_height = 6.0
rib_offset = 10.0

result = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges()
    .fillet(fillet_radius)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

result = (
    result
    .faces(">X")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

rib1 = (
    result
    .faces("<Z")
    .workplane()
    .rect(block_length - 2 * rib_offset, rib_thickness)
    .extrude(rib_height)
)

rib2 = (
    result
    .faces("<Z")
    .workplane()
    .rect(rib_thickness, block_width - 2 * rib_offset)
    .extrude(rib_height)
)

result = result.union(rib1).union(rib2)

result = result.edges("|Z").chamfer(chamfer_distance)
