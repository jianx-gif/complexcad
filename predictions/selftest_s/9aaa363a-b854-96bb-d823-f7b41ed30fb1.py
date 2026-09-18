import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
skirt_height = 6.0
skirt_thickness = 4.0
cavity_diameter = 30.0
cavity_depth = 6.0
screw_hole_diameter = 4.0
screw_spacing = 10.0
number_of_screws = 8
fillet_radius = 2.0
counterbore_diameter = 6.5
counterbore_depth = 3.0

result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z").workplane()
    .rect(plate_length - 2 * skirt_thickness, plate_width - 2 * skirt_thickness)
    .extrude(skirt_height)
    .edges("|Z").fillet(fillet_radius)
    .faces(">Z").workplane()
    .circle(cavity_diameter / 2)
    .cutBlind(-cavity_depth)
    .faces(">Z").workplane()
    .center(0, plate_width / 2 - skirt_thickness - screw_hole_diameter)
    .rarray(screw_spacing, 0, number_of_screws, 1)
    .cboreHole(screw_hole_diameter / 2, counterbore_diameter / 2, counterbore_depth)
)
