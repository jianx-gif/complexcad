import cadquery as cq
BS = cq.selectors.BoxSelector

plate_length = 80.0
plate_width = 50.0
plate_thickness = 10.0
slot_length = 60.0
slot_width = 10.0
blind_hole_diameter = 6.0
blind_hole_depth = 8.0
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 12.0
rib_width = 12.0
rib_height = 20.0
rib_thickness = 5.0
rib_offset = 8.0

base_plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness, centered=(True, True, False))

slot_cut = (
    cq.Workplane("XY")
    .center(0, 0)
    .moveTo(-slot_length/2, -slot_width/2)
    .line(slot_length, 0)
    .line(0, slot_width)
    .line(-slot_length, 0)
    .close()
    .extrude(plate_thickness + 0.2)
)

rib = (
    cq.Workplane("XY")
    .center(plate_length/2 - rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

result = (
    base_plate
    .cut(slot_cut)
    .union(rib)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(blind_hole_diameter, depth=blind_hole_depth)
    .faces("<Z")
    .workplane()
    .pushPoints([
        (plate_length/2 - mount_hole_offset, plate_width/2 - mount_hole_offset),
        (-plate_length/2 + mount_hole_offset, plate_width/2 - mount_hole_offset),
        (-plate_length/2 + mount_hole_offset, -plate_width/2 + mount_hole_offset),
        (plate_length/2 - mount_hole_offset, -plate_width/2 + mount_hole_offset)
    ])
    .hole(mount_hole_diameter)
    .edges(BS((-plate_length/2-0.1, -plate_width/2-0.1, -100), (plate_length/2+0.1, plate_width/2+0.1, 100)))
    .chamfer(chamfer_size)
)
