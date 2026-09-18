import cadquery as cq

plate_width = 60.0
plate_height = 30.0
plate_thickness = 8.0
knuckle_radius = 10.0
knuckle_length = 12.0
chamfer_distance = 0.5
m3_hole_diameter = 3.0
head_diameter = 5.5
countersink_angle = 90.0
mount_hole_diameter = 4.0
mount_spacing_x = 40.0
mount_spacing_y = 20.0
rib_width = 5.0
rib_height = 6.0
slot_width = 6.0
slot_length = 20.0
pocket_depth = 4.0
overlap = 4.0

base_plate = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)
knuckle = (
    cq.Workplane("XY")
    .circle(knuckle_radius)
    .extrude(knuckle_length)
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .translate((0, plate_thickness/2 + knuckle_length/2 - overlap, 0))
)
part = base_plate.union(knuckle)
part = (
    part
    .faces(">Y")
    .workplane()
    .cskHole(m3_hole_diameter, head_diameter, countersink_angle, plate_thickness)
)
mount_pts = [
    (-mount_spacing_x/2, -mount_spacing_y/2),
    (mount_spacing_x/2, -mount_spacing_y/2),
    (-mount_spacing_x/2, mount_spacing_y/2),
    (mount_spacing_x/2, mount_spacing_y/2),
]
part = (
    part
    .faces(">Z")
    .workplane()
    .pushPoints(mount_pts)
    .hole(mount_hole_diameter)
)
part = (
    part
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-plate_thickness/2)
)
part = (
    part
    .faces("<Z")
    .workplane()
    .rect(plate_width-10, plate_height-10)
    .cutBlind(-pocket_depth)
)
rib_spacing = 15.0
num_ribs = int(plate_width // rib_spacing)
rib_pts = [(-(plate_width/2) + rib_spacing/2 + i*rib_spacing, 0) for i in range(num_ribs)]
ribs = (
    cq.Workplane("XY")
    .pushPoints(rib_pts)
    .rect(rib_width, rib_height)
    .extrude(-rib_width)
    .translate((0, -plate_thickness/2, 0))
)
part = part.union(ribs)
part = part.edges("|Y").chamfer(chamfer_distance)
result = part
