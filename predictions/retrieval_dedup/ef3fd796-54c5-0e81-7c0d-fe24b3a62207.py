
import cadquery as cq

block_length = 80
block_width = 50
block_thickness = 10
pocket_length = 30
pocket_width = 20
slot_length = 70
slot_width = 10
slot_angle = 45
slot_depth = 8
rib_length = 40
rib_width = 10
rib_height = 4
clip_hole_diameter = 6
clip_hole_offset_y = -15
mount_hole_diameter = 4
mount_spacing_x = block_width - 20
mount_spacing_y = block_length - 20
chamfer_size = 0.5

base_block = (
    cq.Workplane("XY")
    .sketch()
    .rect(block_width, block_length)
    .rect(pocket_width, pocket_length, mode="s")
    .finalize()
    .extrude(block_thickness)
    .edges()
    .chamfer(chamfer_size)
)

slot_cut = (
    base_block.faces(">Z")
    .workplane()
    .sketch()
    .slot(slot_length, slot_width, angle=slot_angle)
    .finalize()
    .cutBlind(-slot_depth)
)

raised_edge = (
    slot_cut.faces(">Z")
    .workplane()
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

combined = slot_cut.union(raised_edge)

combined = (
    combined.faces(">Z")
    .workplane()
    .center(0, clip_hole_offset_y)
    .hole(clip_hole_diameter)
)

combined = (
    combined.faces(">Z")
    .workplane()
    .rarray(mount_spacing_x, mount_spacing_y, 2, 2)
    .hole(mount_hole_diameter)
)

result = combined
