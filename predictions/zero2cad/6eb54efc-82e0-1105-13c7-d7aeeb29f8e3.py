import cadquery as cq

bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
slot_length = 40.0
slot_width = 8.0
hole_diameter = 6.0
hole_clearance = 2.0
hole_spacing = 30.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 20.0
chamfer_distance = 1.0

base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

slot_cut = (
    base.faces("<Y")
    .workplane()
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-bracket_thickness)
)

hole_positions = [
    (-hole_spacing, 0),
    (0, 0),
    (hole_spacing, 0)
]

holes = (
    slot_cut.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter + hole_clearance)
)

rib_count = int((bracket_length - 2 * rib_spacing) // rib_spacing) + 1
rib_positions = [(-bracket_length/2 + rib_spacing + i * rib_spacing, 0) for i in range(rib_count)]

ribs = (
    holes.faces(">Z")
    .workplane()
    .pushPoints(rib_positions)
    .rect(rib_width, bracket_width - 2 * rib_spacing)
    .cutBlind(-rib_height)
)

result = (
    ribs.edges()
    .chamfer(chamfer_distance)
)
