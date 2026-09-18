import cadquery as cq
knob_radius = 20.0
knob_length = 50.0
wall_thickness = 2.0
flange_radius = 30.0
flange_thickness = 8.0
flange_thickness = 10.0
flange_radius = flange_radius - 2.0
flange_thickness = 8.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(flange_radius, 0)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + fl.flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, fl.flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flange_thickness)
    .lineTo(flange_radius, flange_thickness + flflange_thickness)
    .lineTo(flange_radius, fl.flange_thickness + flflange_thickness)
    .lineTo(flange_radius, flange_thickness + fl.flange_thickness)
    .lineTo(flange_radius, fl.flange_thickness + flange_thickness))
    .lineTo(flange_radius, 0)
    .lineTo(0, 0)
    .close()
)
result = (
    profile
    .revolve(360)
    .workplane()
    .center(0, 0)
    .rect(flange_thickness, fl2*flange_thickness)
    .cutBlind(-flange_thickness)
)
