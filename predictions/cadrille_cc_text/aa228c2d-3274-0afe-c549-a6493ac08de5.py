import cadquery as cq
horizontal_leg_length = 70.0
vertical_leg_height = 80.0
leg_thickness = 10.0
leg_thickness = 8.0
bracket_thickness = 5.0
inner_fillet_radius = 3.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_edge_distance = 10.0
gusset_length = 20.0
gusset_thickness = 5.0
gusset_thickness = bracket_thickness
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (horizontal_leg_length, 0),
        (horizontal_leg_length, leg_thickness),
        (leg_thickness, leg_thickness),
        (leg_thickness, leg_thickness),
        (0, leg_thickness),
    ])
    .close()
    .extrude(bracket_thickness)
    .edges("|Z")
    .fillet(inner_fillet_radius)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .polyline([
        (0, 0),
        (leg_thickness, 0),
        (leg_thickness, leg_thickness),
        (0, leg_thickness),
    ])
    .close()
    .extrude(bracket_thickness)
    .edges("|Z")
    .fillet(gusset_thickness)
    .faces(">Z")
    .workplane()
    .center(hole_edge_distance, hole_edge_distance)
    .hole(hole_diameter)
    .center(hole_edge_distance, hole_edge_distance)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(hole_edge_distance, hole_edge_distance)
    .hole(hole_diameter)
    .center(hole_edge_distance, hole_edge_distance)
    .hole(hole_diameter)
    .faces("<Z")
    .edges()
    .fillet(leg_thickness)
)
