import cadquery as cq

knob_max_radius = 25.0
knob_min_radius = 10.0
knob_height = 30.0
shoulder_height = 5.0
base_height = 12.0
center_hole_radius = 3.0
set_screw_radius = 2.0
set_screw_offset = 12.0

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(knob_min_radius, 0)
    .lineTo(knob_min_radius, base_height)
    .lineTo(knob_max_radius, base_height + shoulder_height)
    .lineTo(knob_max_radius, knob_height)
    .lineTo(0, knob_height)
    .close()
)

result = profile.revolve()

center_hole = (
    cq.Workplane("XY")
    .circle(center_hole_radius)
    .extrude(knob_height)
)
result = result.cut(center_hole)

set_screw = (
    cq.Workplane("XY")
    .center(set_screw_offset, 0)
    .circle(set_screw_radius)
    .extrude(knob_height)
)
result = result.cut(set_screw)
