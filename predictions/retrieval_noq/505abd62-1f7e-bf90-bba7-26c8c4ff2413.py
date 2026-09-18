import cadquery as cq

plate_width = 80
plate_length = 120
plate_thickness = 6
central_cut_width = 30
central_cut_length = 40
hole_pitch = 20
hole_rows = 4
hole_cols = 5
clearance_hole_diameter = 6
slot_length = 70
slot_width = 4
slot_offset_from_center = 30
fillet_radius = 2
chamfer_size = 0.8

result = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness)
    .edges("|Z").fillet(fillet_radius)
    .faces(">Z").workplane()
    .center(0, 0)
    .rect(central_cut_width, central_cut_length)
    .cutThruAll()
    .faces(">Z").workplane()
    .rarray(hole_pitch, hole_pitch, hole_cols, hole_rows, True)
    .hole(clearance_hole_diameter / 2)
    .faces("<X").workplane(centerOption="CenterOfMass", invert=True)
    .center(0, slot_offset_from_center)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
    .faces(">Z").edges().chamfer(chamfer_size)
)
