import cadquery as cq
import math

base_length = 80.0
base_width = 60.0
base_thickness = 5.0
frame_height = 8.0
frame_margin = 5.0
hole_diameter = 4.0
countersink_diameter = 6.0
countersink_angle = 90.0
hole_pattern_radius = 20.0
rib_thickness = 3.0
rib_width = 8.0
rib_count = 2
rib_spacing = (base_width - rib_count * rib_width) / (rib_count + 1)
rib_length = base_length - 2 * frame_margin
inner_length = base_length - 2 * frame_margin
inner_width = base_width - 2 * frame_margin

hole_positions = [
    (hole_pattern_radius * math.cos(math.radians(a)), hole_pattern_radius * math.sin(math.radians(a)))
    for a in (0, 90, 180, 270)
]

base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)

outer_frame = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(base_length, base_width)
    .extrude(frame_height)
)

inner_frame = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(inner_length, inner_width)
    .extrude(frame_height)
)

frame = outer_frame.cut(inner_frame)

combined = base.union(frame)

with_holes = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, base_thickness + frame_height)
)

result = (
    with_holes
    .faces("<Z")
    .workplane()
    .rarray(rib_width + rib_spacing, 0, rib_count, 1, center=True)
    .rect(rib_width, rib_length)
    .extrude(-rib_thickness)
)
