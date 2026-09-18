import cadquery as cq
outer_radius = 30.0
housing_length = 60.0
flange_width = 15.0
flange_height = 10.0
wall_thickness = 2.0
flange_hole_diameter = 6.0
flange_hole_spacing = 40.0
flange_hole_count = 4
flange_hole_spacing = flange_hole_count
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, housing_length - flange_height)
    .lineTo(flange_hole_spacing, housing_length - flange_height)
    .lineTo(flange_hole_spacing, housing_length)
    .lineTo(0, housing_length)
    .close()
)
result = (
    profile
    .revolve()
    .shell(-wall_thickness)
    .edges()
    .chamfer(flange_hole_diameter)
)
