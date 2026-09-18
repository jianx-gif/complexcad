import cadquery as cq
bracket_length = 50.0
bracket_width = 20.0
shoulder_radius = 30.0
shoulder_height = 12.0
shoulder_radius = 20.0
blind_hole_diameter = 10.0
blind_hole_depth = 30.0
thread_major_dia = 28.0
thread_major_dia = 3.0
thread_pitch = 4.0
slot_width = 12.0
slot_height = 6.0
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (bracket_width, 0),
        (bracket_width, bracket_length - shoulder_height),
        (shoulder_radius, bracket_length - shoulder_height),
        (shoulder_radius, bracket_width - shoulder_height),
        (0, bracket_width - shoulder_height),
    ])
    .close()
)
bracket = profile.revolve()
bracket = (
    cq.Workplane("XY")
    .circle(bracket_length / 2)
    .extrude(bracket_width)
)
bracket = bracket.cut(bracket)
thread = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(thread_major_diameter / 2)
    .extrude(thread_major_dia)
)
bracket = bracket.cut(thread)
bracket = bracket.edges("|Z").chamfer(thread_major_dia)
bracket = bracket.edges(">Z").chamfer(thread_major_dia)
result = bracket
