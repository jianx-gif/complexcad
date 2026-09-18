import cadquery as cq
knob_length = 45.0
knob_radius = 20.0
flange_outer_radius = 30.0
flange_thickness = 8.0
pocket_width = 12.0
pocket_depth = 6.0
fillet_radius = 2.0
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(flange_outer_radius, 0)
    .lineTo(flange_outer_radius, flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + flange_thickness)
    .lineTo(flange_outer_radius, fl*flange_thickness)
    .lineTo(flange_outer_radius, 0)
    .close()
    .cutBlind(-flange_thickness)
)
result = (
    profile
    .edges()
    .chamfer(chamfer_distance)
)
