import cadquery as cq
flange_length = 60.0
flange_width = 30.0
flange_thickness = 8.0
vertical_leg_height = 40.0
pocket_width = 6.0
pocket_length = 30.0
pocket_depth = 4.0
hole_diameter = 6.0
countersink_diameter = 10.0
countersink_angle = 90.0
fillet_radius = 1.0
rib_width = 4.0
rib_depth = 2.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing = 20.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (flange_width, 0),
        (flange_width, flange_thickness),
        (flange_width + flange_thickness, flange_thickness),
        (flange_width + flange_thickness, flange_length - flange_thickness),
        (0, flange_length - flange_thickness),
        (0, 0)
    ])
    .close()
    .extrude(flange_thickness)
)
result = (
    base
    .faces(">Z")
    .workplane()
    .center(flange_width/2 - pocket_width/2, 0)
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_depth)
    .cutBlind(-rib_depth)
    .edges("|Z")
    .fillet(fillet_radius)
    .edges("|Z")
    .chamfer(fillet_radius)
)
