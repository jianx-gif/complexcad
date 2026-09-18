import cadquery as cq

# Dimensions
base_length = 80.0
base_width = 60.0
base_thickness = 8.0
frame_outer_length = 72.0
frame_outer_width = 52.0
frame_height = 6.0
frame_wall_thickness = 4.0
central_recess_radius = 15.0
central_recess_depth = 6.0
screw_hole_diameter = 2.0
countersink_diameter = 4.0
countersink_depth = 2.5
screw_count = 8
screw_spacing = 10.0
screw_offset_y = 20.0
edge_fillet = 2.0

result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .rect(frame_outer_length, frame_outer_width)
    .extrude(frame_height)
    .faces(">Z")
    .workplane()
    .rect(frame_outer_length - 2 * frame_wall_thickness, frame_outer_width - 2 * frame_wall_thickness)
    .cutBlind(frame_height)
    .edges("|Z")
    .fillet(edge_fillet)
    .faces(">Z")
    .workplane()
    .circle(central_recess_radius)
    .cutBlind(-central_recess_depth)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-(screw_count - 1) / 2 * screw_spacing + i * screw_spacing, screw_offset_y)
        for i in range(screw_count)
    ])
    .cboreHole(screw_hole_diameter, countersink_diameter, countersink_depth)
)
