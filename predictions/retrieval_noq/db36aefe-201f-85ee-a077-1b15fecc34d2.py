import cadquery as cq

knob_outer_radius = 25.0
knob_height = 20.0
knob_base_height = 5.0
knob_grip_radius = 30.0
shaft_radius = 8.0
shaft_length = 15.0
set_screw_diameter = 3.0
calibration_groove_width = 6.0
calibration_groove_depth = 1.5
base_chamfer = 1.5
inner_pocket_width = 8.0
inner_pocket_depth = 2.0

result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(knob_outer_radius, 0)
    .lineTo(knob_outer_radius, knob_base_height)
    .threePointArc((knob_outer_radius * 1.1, knob_base_height + 2), (knob_grip_radius, knob_height * 0.6))
    .lineTo(knob_grip_radius, knob_height)
    .lineTo(0, knob_height)
    .close()
    .revolve()
    .faces("<Z")
    .workplane()
    .tag("knob_base")
    .workplaneFromTagged("knob_base")
    .circle(shaft_radius)
    .extrude(-shaft_length)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(calibration_groove_width, calibration_groove_depth)
    .cutBlind(-calibration_groove_depth)
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .rect(inner_pocket_width, inner_pocket_depth)
    .cutBlind(-inner_pocket_depth)
    .faces("<Z")
    .workplane()
    .hole(set_screw_diameter)
    .edges("<Z").chamfer(base_chamfer)
)
