import cadquery as cq

knob_outer_radius = 20.0
knob_base_height = 12.0
knob_shoulder_radius = 12.0
knob_shoulder_height = 8.0
shaft_radius = 4.0
mount_hole_radius = 2.0
mount_hole_circle_radius = 14.0
fillet_radius = 2.0
chamfer_size = 1.0

base = (
    cq.Workplane("XY")
    .circle(knob_outer_radius)
    .extrude(knob_base_height)
    .faces(">Z")
    .workplane()
    .tag("top_base")
)

with_holes = (
    base
    .workplaneFromTagged("top_base")
    .polarArray(radius=mount_hole_circle_radius, startAngle=0, angle=360/6, count=6)
    .hole(mount_hole_radius * 2)
)

shoulder = (
    with_holes
    .faces(">Z")
    .workplane()
    .circle(knob_shoulder_radius)
    .extrude(knob_shoulder_height)
)

result = (
    shoulder
    .hole(shaft_radius * 2)
)

result = result.edges("|Z").fillet(fillet_radius)
result = result.edges("<Z").chamfer(chamfer_size)
