import cadquery as cq

# Parameters
knob_outer_radius = 30.0
knob_base_radius = 15.0
knob_total_height = 40.0
base_height = 5.0
shoulder_height = 10.0
shoulder_radius = 22.0
fillet_radius = 2.0
split_key_width = 4.0
split_key_depth = 5.0
split_key_angle = 30.0
pin_hole_radius = 2.0

# Profile definition
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(knob_base_radius, 0)
    .lineTo(knob_base_radius, base_height)
    .lineTo(shoulder_radius, base_height + shoulder_height)
    .lineTo(knob_outer_radius, knob_total_height)
    .lineTo(0, knob_total_height)
    .close()
)

knob = profile.revolve()

# Apply fillet to all edges (should succeed now)
knob = knob.edges().fillet(fillet_radius)

slot = (
    cq.Workplane("XY")
    .box(split_key_width, knob_outer_radius * 2, split_key_depth)
    .rotate((0, 0, 0), (0, 0, 1), split_key_angle)
    .translate((0, 0, base_height + shoulder_height/2))
)
knob = knob.cut(slot)

pin_hole = (
    cq.Workplane("XY")
    .circle(pin_hole_radius)
    .extrude(knob_total_height + 2)
)
knob = knob.cut(pin_hole)

result = knob