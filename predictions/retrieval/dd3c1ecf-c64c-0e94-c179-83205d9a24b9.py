import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 6.0
chamfer_size = 1.0
hole_diameter = 12.0
hole_depth = 4.0
edge_clearance = 5.0
rib_thickness = 4.0
rib_height = 2.0
rib_spacing = 20.0
central_cut_width = 30.0
central_cut_height = 20.0
slot_length = 15.0
slot_width = 5.0

profile = (
    cq.Sketch()
    .rect(plate_length, plate_width)
    .rect(central_cut_width, central_cut_height, mode="s")
)

base_plate = (
    cq.Workplane("XY")
    .placeSketch(profile)
    .extrude(plate_thickness)
)

base_plate = base_plate.edges("|Z").chamfer(chamfer_size)

slot_positions = [
    (-plate_length/2 + edge_clearance + slot_length/2, 0),
    (plate_length/2 - edge_clearance - slot_length/2, 0)
]

for x, y in slot_positions:
    base_plate = (
        base_plate
        .faces(">Z")
        .workplane(centerOption="CenterOfMass", origin=(x, y, plate_thickness))
        .rect(slot_length, slot_width)
        .cutBlind(-plate_thickness)
    )

hole_positions = [
    (-plate_length/2 + edge_clearance + 15, 0),
    (0, plate_width/2 - edge_clearance - 15),
    (plate_length/2 - edge_clearance - 15, 0)
]

for x, y in hole_positions:
    base_plate = (
        base_plate
        .faces("<Z")
        .workplane(centerOption="CenterOfMass", origin=(x, y, plate_thickness))
        .hole(hole_diameter, depth=hole_depth)
    )

rib_profile = cq.Sketch().rect(rib_thickness, rib_spacing)

rib = (
    cq.Workplane("XY")
    .placeSketch(rib_profile)
    .extrude(rib_height)
)

rib_count = int((plate_width - 2*edge_clearance) // rib_spacing)

for i in range(rib_count):
    y = -plate_width/2 + edge_clearance + rib_spacing/2 + i * rib_spacing
    base_plate = base_plate.union(rib.translate((0, y, 0)))

result = base_plate