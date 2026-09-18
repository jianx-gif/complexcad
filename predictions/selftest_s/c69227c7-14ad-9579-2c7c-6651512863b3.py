import cadquery as cq
import math

knob_head_radius = 20.0
knob_head_height = 12.0
stem_base_radius = 12.0
stem_top_radius = 6.0
stem_height = 15.0
central_hole_diameter = 8.0
torque_slot_width = 4.0
torque_slot_length = 18.0
slot_radial_offset = 10.0
fillet_radius = 1.0
chamfer_depth = 1.0
mounting_hole_radius = 2.0
mounting_hole_count = 4
mounting_hole_circle_radius = 15.0

stem_taper_angle = math.degrees(math.atan((stem_top_radius - stem_base_radius) / stem_height))

result = (
    cq.Workplane("XY")
    .circle(knob_head_radius)
    .extrude(knob_head_height)
    .faces(">Z")
    .workplane()
    .tag("head_top")
    .workplaneFromTagged("head_top")
    .circle(stem_base_radius)
    .extrude(stem_height, taper=stem_taper_angle)
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
)

slot_cut = (
    cq.Workplane("XZ")
    .center(0, knob_head_radius - slot_radial_offset)
    .rect(torque_slot_length, torque_slot_width)
    .extrude(2 * knob_head_radius)
)
result = result.cut(slot_cut)

mounting_points = [
    (
        mounting_hole_circle_radius * math.cos(2 * math.pi * i / mounting_hole_count),
        mounting_hole_circle_radius * math.sin(2 * math.pi * i / mounting_hole_count),
    )
    for i in range(mounting_hole_count)
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(mounting_points)
    .hole(mounting_hole_radius * 2)
)

result = result.edges("<Z").chamfer(chamfer_depth)
result = result.edges("<<Z").fillet(fillet_radius)
