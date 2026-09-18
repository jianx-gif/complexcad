import cadquery as cq
import math

outer_radius = 30.0
outer_height = 25.0
shaft_radius = 8.0
shaft_height = 10.0
dome_height = 8.0
insert_radius = 3.0
insert_length = 12.0
chamfer_size = 1.0
grip_ring_radius = 25.0
grip_ring_thickness = 2.0
grip_ring_depth = 4.0
peripheral_hole_radius = 1.5
peripheral_hole_count = 6

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_radius, 0)
    .lineTo(shaft_radius, shaft_height)
    .threePointArc(
        (outer_radius, shaft_height + (outer_height - shaft_height - dome_height) / 2),
        (outer_radius, outer_height - dome_height)
    )
    .lineTo(0, outer_height)
    .close()
)

knob_body = profile.revolve()

knob_body = (
    knob_body
    .workplane(offset=outer_height)
    .center(0, 0)
    .circle(insert_radius)
    .cutBlind(-insert_length)
)

knob_body = (
    knob_body
    .workplane(offset=outer_height - grip_ring_depth)
    .center(0, 0)
    .circle(grip_ring_radius)
    .circle(grip_ring_radius - grip_ring_thickness)
    .cutBlind(-grip_ring_depth)
)

angle_step = 360.0 / peripheral_hole_count
hole_positions = [
    (
        (grip_ring_radius - grip_ring_thickness / 2) * math.cos(math.radians(i * angle_step)),
        (grip_ring_radius - grip_ring_thickness / 2) * math.sin(math.radians(i * angle_step))
    )
    for i in range(peripheral_hole_count)
]

knob_body = (
    knob_body
    .workplane(offset=outer_height - grip_ring_depth/2)
    .pushPoints(hole_positions)
    .hole(peripheral_hole_radius * 2)
)

knob_body = knob_body.edges().first().chamfer(chamfer_size)

result = knob_body