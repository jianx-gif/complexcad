import cadquery as cq

plate_width = 80.0
plate_height = 80.0
plate_thickness = 5.0
boss_diameter = 25.0
boss_height = 12.0
boss_recess_depth = 4.0
slot_width = 6.0
slot_length = 30.0
slot_offset = 20.0
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_offset = 10.0

base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges()
    .chamfer(chamfer_size)
)

boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, plate_thickness))
)

recess = (
    cq.Workplane("XY")
    .circle((boss_diameter - 4) / 2)
    .extrude(boss_recess_depth)
    .translate((0, 0, plate_thickness + boss_height - boss_recess_depth))
)

slot_profile = (
    cq.Workplane("XY")
    .rect(slot_length, slot_width)
    .extrude(plate_thickness + 0.1)
)

slot1 = slot_profile.translate((slot_offset, 0, 0))
slot2 = slot_profile.translate((-slot_offset, 0, 0))
slot3 = slot_profile.translate((0, slot_offset, 0))
slot4 = slot_profile.translate((0, -slot_offset, 0))

mount_hole = (
    cq.Workplane("XY")
    .circle(mount_hole_dia / 2)
    .extrude(plate_thickness + 0.1)
)

hole1 = mount_hole.translate((mount_hole_offset, mount_hole_offset, 0))
hole2 = mount_hole.translate((-mount_hole_offset, mount_hole_offset, 0))
hole3 = mount_hole.translate((mount_hole_offset, -mount_hole_offset, 0))
hole4 = mount_hole.translate((-mount_hole_offset, -mount_hole_offset, 0))

result = (
    base
    .union(boss)
    .cut(recess)
    .cut(slot1)
    .cut(slot2)
    .cut(slot3)
    .cut(slot4)
    .cut(hole1)
    .cut(hole2)
    .cut(hole3)
    .cut(hole4)
)
