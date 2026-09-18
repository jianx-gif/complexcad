import cadquery as cq
plate_width = 80.0
plate_depth = 50.0
plate_thickness = 5.0
edge_fillet = 2.0
chamfer = 0.5
stud_diameter = 6.0
stud_height = 4.0
stud_depth = 2.0
stiff_diameter = 5.0
stiff_height = 10.0
stiff_start = 50.0
rib_height = plate_thickness + 2 * edge_fillet
rib_length = plate_width - 2 * rib_height
rib_start = 0
rib_end = 0
rib_end = 0
rib_start = 0
rib_end = 0
rib_end = 0
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z")
    .fillet(edge_fillet)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(stiff_diameter, stud_diameter, stud_height)
    .edges("|Z")
    .chamfer(chamfer)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(stiff_diameter, stud_depth, stud_height)
)
