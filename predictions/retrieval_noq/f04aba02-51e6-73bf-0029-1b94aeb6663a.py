import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
hole_diameter = 8.0
hole_spacing_x = 50.0
hole_spacing_y = 30.0
logo_text = "LOGO"
logo_fontsize = 20.0
logo_height = 1.5
fillet_radius = 1.0
chamfer_distance = 0.5

# Base plate with outer fillet
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Mounting holes and top chamfer
with_holes = (
    base
    .faces("<Z")
    .workplane()
    .pushPoints([(-hole_spacing_x/2, -hole_spacing_y/2),
                 ( hole_spacing_x/2, -hole_spacing_y/2),
                 ( hole_spacing_x/2,  hole_spacing_y/2),
                 (-hole_spacing_x/2,  hole_spacing_y/2)])
    .hole(hole_diameter)
    .edges(">Z")
    .chamfer(chamfer_distance)
)

# Embossed logo on top surface
logo = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, plate_thickness))
    .text(logo_text, logo_fontsize, logo_height)
)

result = with_holes.union(logo)
