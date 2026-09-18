import cadquery as cq

outer_diameter = 40
inner_diameter = 20
flange_thickness = 5
flange_width = 12
length = 80
chamfer_dist = 1.5
hole_diameter = 3
pattern_spacing = 10
pattern_cols = 3
pattern_rows = 3

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

outer_body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, length)
    .lineTo(outer_radius + flange_thickness, length)
    .lineTo(outer_radius + flange_thickness, length + flange_width)
    .lineTo(0, length + flange_width)
    .close()
    .revolve(360)
)

inner_cylinder = cq.Workplane("XY").cylinder(length + flange_width, inner_radius)

base = outer_body.cut(inner_cylinder)

result = (
    base
    .edges("<Z")
    .chamfer(chamfer_dist)
    .faces(">Z")
    .workplane()
    .rarray(pattern_spacing, pattern_spacing, pattern_cols, pattern_rows)
    .hole(hole_diameter)
)
