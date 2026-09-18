import cadquery as cq
bracket_height = 60.0
bracket_thickness = 5.0
outer_radius = 30.0
tab_height = 20.0
tab_thickness = bracket_thickness
hole_diameter = 5.0
hole_spacing = 15.0
hole_count = 4
tab_angle = 60.0
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (outer_radius, 0),
        (outer_radius, tab_height),
        (tab_thickness, tab_height),
        (tab_thickness, tab_height),
        (0, tab_height),
    ])
    .close()
    .revolve()
)
result = (
    profile
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
