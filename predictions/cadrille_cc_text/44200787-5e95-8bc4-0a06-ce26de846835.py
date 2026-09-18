import cadquery as cq
vertical_width = 20.0
vertical_length = 70.0
vertical_thickness = 8.0
horizontal_width = 20.0
horizontal_length = 90.0
mount_hole_diameter = 5.0
mount_hole_count = 4
slot_length = 30.0
slot_width = 5.0
slot_depth = 6.0
rib_width = 4.0
rib_length = 60.0
rib_center_x = 30.0
rib_center_y = 35.0
chamfer = 0.5
base = (
    cq.Workplane("XY")
    .box(vertical_width, vertical_length, vertical_thickness)
    .edges("|Z")
    .chamfer(chamfer)
)
slot = (
    cq.Workplane("XY")
    .box(vertical_width, vertical_length, slot_depth)
    .translate((0, vertical_length / 2, 0))
)
rib = (
    cq.Workplane("XY")
    .box(vertical_width, vertical_length, rib_thickness)
    .translate((0, vertical_length / 2, 0))
)
rib = rib.union(slot)
rib = rib.translate((0, vertical_length / 2, 0))
rib = rib.translate((0, vertical_length / 2, 0))
rib = rib.translate((0, vertical_length / 2, 0))
result = base.union(rib)
result = result.faces(">Z").workplane().hole(mount_hole_diameter)
result = result.faces(">Z").workplane().center(0, 0).rect(slot_length, slot_width).cutBlind(-slot_depth)
result = result.faces(">Z").workplane().center(0, 0).rect(slot_length, slot_width).cutBlind(-slot_depth)
