import cadquery as cq

plate_length = 100.0
plate_width = 60.0
plate_thickness = 10.0
pocket_length = 80.0
pocket_width = 40.0
pocket_depth = 4.0
slot_width = 5.0
slot_height = 20.0
slot_depth = 8.0
number_slots = 5
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_dia = 5.0
hole_offset = 5.0
rib_width = 5.0
rib_length = plate_length - 20.0
rib_height = 2.0
gusset_height = 3.0

result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rect(pocket_length, pocket_width)
    .cutBlind(pocket_depth)
)

slot_spacing = plate_length / (number_slots + 1)
slot_positions = [(-plate_length/2 + slot_spacing*(i+1), 0) for i in range(number_slots)]
for x, y in slot_positions:
    result = (
        result.faces(">Z").workplane()
        .center(x, y)
        .rect(slot_width, slot_height)
        .cutBlind(slot_depth)
    )

result = result.faces(">Z").edges().fillet(fillet_radius)
result = result.faces("<Z").edges().chamfer(chamfer_distance)

corner_points = [
    ( plate_length/2 - hole_offset,  plate_width/2 - hole_offset),
    (-plate_length/2 + hole_offset,  plate_width/2 - hole_offset),
    (-plate_length/2 + hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset, -plate_width/2 + hole_offset)
]
result = (
    result.faces(">Z").workplane()
    .pushPoints(corner_points)
    .hole(mount_hole_dia)
)

rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

points = [(-plate_length/2 + 10, -plate_width/2 + 10), ( -plate_length/2 + 30, -plate_width/2 + 10), (-plate_length/2 + 10, -plate_width/2 + 30)]

gusset = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(gusset_height)
)

result = result.union(rib).union(gusset)
