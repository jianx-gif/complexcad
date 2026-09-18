import cadquery as cq

# Parameters
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 5.0
tab_width = 20.0
tab_height = 15.0
slot_length = 40.0
slot_width = 8.0
hole_diameter = 6.0
hole_depth = 3.0
hole_pattern_radius = 25.0
chamfer_size = 0.5

# Base plate with side tab
base_plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)

tab = (
    cq.Workplane("XY")
    .center(plate_width/2 + tab_width/2, 0)
    .rect(tab_width, tab_height)
    .extrude(plate_thickness)
)

result = (
    base_plate.union(tab)
    .edges("|Z").chamfer(chamfer_size)
    .faces(">Z").workplane()
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
    .faces(">Z").workplane()
    .polarArray(hole_pattern_radius, 0, 360, 6)
    .circle(hole_diameter/2)
    .cutBlind(-hole_depth)
)
