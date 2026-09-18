import cadquery as cq
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
shoulder_width = 30.0
shoulder_height = 15.0
hole_diameter = 4.5
hole_spacing = 30.0
hole_count = 6
edge_chamfer = 1.0
relief_radius = 10.0
relief_depth = 6.0
rib_width = 5.0
rib_height = 3.0
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(hole_diameter / 2)
    .cutBlind(-bracket_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.edges("|Z").chamfer(edge_chamfer)
result = base
