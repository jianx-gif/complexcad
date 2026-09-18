import cadquery as cq
block_length = 80.0
block_width = 50.0
block_height = 20.0
fillet_radius = 3.0
cavity_length = 60.0
cavity_width = 30.0
cavity_depth = 12.0
counterbore_head_dia = 15.0
counterbore_head_depth = 8.0
counterbore_depth = 2.0
mounting_hole_dia = 5.0
mounting_hole_spacing = 40.0
chamfer_size = 1.0
rib_thickness = 4.0
rib_height = 6.0
rib_length = block_length - 2 * rib_thickness
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .hole(cavity_length)
    .faces(">Z")
    .workplane()
    .hole(counterbore_head_dia, depth=counterbore_depth)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(counterbore_head_dia, depth=counterbore_depth)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(counterbore_head_dia, depth=counterbore_depth)
    .center(0, 0)
    .rect(rib_length, block_width)
    .extrude(rib_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_length, block_width)
    .extrude(rib_thickness)
    .translate((0, 0, block_height - rib_thickness))
)
result = base.union(rib)
