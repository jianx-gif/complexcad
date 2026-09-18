import cadquery as cq

# Parameters
plate_width = 80.0
plate_height = 60.0
plate_thickness = 5.0
tab_width = 20.0
tab_length = 10.0
slot_length = 40.0
slot_width = 8.0
hole_diameter = 6.0
blind_hole_depth = 3.0
peripheral_radius = 30.0
num_holes = 8
edge_chamfer = 0.5

# Base plate with side tab
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .center(plate_width / 2 + tab_width / 2, 0)
    .rect(tab_width, tab_length)
)

result = (
    base
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(edge_chamfer)
    .faces(">Z")
    .workplane()
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .polarArray(peripheral_radius, 0, 360, num_holes)
    .hole(hole_diameter, blind_hole_depth)
)
