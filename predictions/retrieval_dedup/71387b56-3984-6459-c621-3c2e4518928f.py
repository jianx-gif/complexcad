import cadquery as cq

arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
inner_cut_length = 60.0
inner_cut_width = 10.0
boss_radius = 8.0
boss_height = 6.0
hole_diameter = 6.0
hole_spacing = 20.0
chamfer_size = 1.0
fillet_radius = 1.0
notch_width = 12.0
notch_depth = 6.0
rib_width = 6.0
rib_height = 4.0
rib_length = 20.0
rib_spacing = 30.0

base_sketch = (
    cq.Sketch()
    .rect(arm_length, arm_width)
    .rect(inner_cut_length, inner_cut_width)
)

result = (
    cq.Workplane("XY")
    .placeSketch(base_sketch)
    .extrude(arm_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
)

hole_positions = [
    (-hole_spacing/2, -hole_spacing/2),
    (hole_spacing/2, -hole_spacing/2),
    (-hole_spacing/2, hole_spacing/2),
    (hole_spacing/2, hole_spacing/2)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

rib_offsets = [-rib_spacing/2, rib_spacing/2]
for x_offset in rib_offsets:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x_offset, 0)
        .rect(rib_length, rib_width)
        .extrude(rib_height)
    )

result = (
    result
    .faces(">X")
    .workplane()
    .center(0, -arm_thickness/2 + notch_depth/2)
    .rect(notch_width, notch_depth)
    .cutBlind(-notch_width)
)

result = result.edges(">Z").fillet(fillet_radius)
