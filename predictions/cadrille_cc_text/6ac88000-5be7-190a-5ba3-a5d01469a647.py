import cadquery as cq
knob_base_radius = 20.0
knob_shoulder_height = 8.0
knob_shoulder_radius = 15.0
knob_shoulder_height = 6.0
clearance_bore_radius = 5.0
clearance_bore_radius = 22.0
clearance_bore_depth = knob_shoulder_height + 2.0
chamfer_distance = 0.8
radial_radius = 25.0
radial_height = 4.0
radial_outer_radius = 25.0
radial_outer_radius = radius.0
radial_height = 4.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(knob_base_radius, 0)
    .lineTo(knob_base_radius, knob_shoulder_height)
    .lineTo(knob_shoulder_radius, knob_shoulder_height)
    .lineTo(knob_shoulder_radius, knob_shoulder_height + knob_shoulder_height)
    .lineTo(knob_shoulder_radius, knob_shoulder_height + knob_shoulder_height)
    .lineTo(knob_shoulder_radius, knob_shoulder_height + knob_shoulder_height)
    .lineTo(knob_shoulder_radius, knob_shoulder_height + knob_shoulder_height)
    .lineTo(0, knob_shoulder_height + knob_shoulder_height)
    .close()
    .revolve()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(rail_outer_radius * 2)
solid = solid.faces(">Z").workplane().circle(rail_outer_radius).cutBlind(-radial_height)
result = solid
