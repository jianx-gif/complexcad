import cadquery as cq
bracket_length = 80.0
bracket_width = 50.0
bracket_thickness = 8.0
cavity_width = 40.0
cavity_height = 30.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset_y = -15.0
fillet_radius = 2.0
chamfer_distance = 0.8
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)
cavity = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(cavity_width, cavity_height)
    .extrude(bracket_thickness)
)
cavity = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(cavity_width, cavity_height)
    .extrude(bracket_thickness)
)
result = base.union(cavity)
result = result.edges("|Z").fillet(fillet_radius)
result = result.edges("|Z").chamfer(chamfer_distance)
