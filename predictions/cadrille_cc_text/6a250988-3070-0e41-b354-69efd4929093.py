import cadquery as cq
chute_length = 40.0
pitch_diameter = 50.0
outer_radius = pitch_diameter / 2.0
draft_angle_deg = 25.0
base_thickness = 5.0
through_hole_diameter = 20.0
counterbore_diameter = 8.0
counterbore_offset = 2.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (chute_length, 0),
        (chute_length, base_thickness),
        (outer_radius, base_thickness),
        (outer_radius, 0),
    ])
    .close()
)
result = (
    profile
    .revolve()
    .edges()
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .cboreHole(through_hole_diameter, counterbore_diameter, counterbore_offset)
)
