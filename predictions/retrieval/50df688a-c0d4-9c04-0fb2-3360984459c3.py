import cadquery as cq

knob_outer_radius = 30.0
knob_height = 25.0
hub_radius = 12.0
hub_height = 6.0
ridge_outer_radius = knob_outer_radius + 2.0
ridge_start = 12.0
ridge_end = 18.0
shaft_hole_radius = 4.0
fillet_radius = 0.8

profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(hub_radius, 0)
    .lineTo(hub_radius, hub_height)
    .lineTo(knob_outer_radius, hub_height)
    .lineTo(knob_outer_radius, ridge_start)
    .lineTo(ridge_outer_radius, ridge_start)
    .lineTo(ridge_outer_radius, ridge_end)
    .lineTo(knob_outer_radius, ridge_end)
    .lineTo(knob_outer_radius, knob_height)
    .lineTo(0, knob_height)
    .close()
)

body = profile.revolve()

body = body.faces("<Z").workplane().hole(shaft_hole_radius * 2)

slot_width = 3.0
slot_length = 10.0
key_slot = (
    cq.Workplane("XY")
    .center(ridge_outer_radius/2, hub_height/2)
    .rect(slot_width, slot_length)
    .extrude(knob_height)
)
body = body.cut(key_slot)

result = body.edges("|Z").fillet(fillet_radius)
