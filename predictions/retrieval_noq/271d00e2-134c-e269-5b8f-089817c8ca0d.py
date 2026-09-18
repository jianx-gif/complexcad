import cadquery as cq

outer_diameter = 80
coupler_length = 100
flange_thickness = 10
flange_extra = 10
bore_diameter_start = 30
bore_diameter_end = 20
keyway_width = 8
keyway_depth = 3
keyway_length = 60
chamfer_size = 2
drill_hole_diameter = 5
drill_hole_spacing = 30
wall_thickness = 5

outer_radius = outer_diameter / 2.0
flange_outer_radius = outer_radius + flange_extra

result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, coupler_length - flange_thickness)
    .lineTo(flange_outer_radius, coupler_length - flange_thickness)
    .lineTo(flange_outer_radius, coupler_length)
    .lineTo(0, coupler_length)
    .close()
    .revolve()
)

result = result.shell(-wall_thickness)

result = result.cut(
    cq.Solid.makeCone(bore_diameter_start / 2.0, bore_diameter_end / 2.0, coupler_length - flange_thickness)
)

keyway = (
    cq.Workplane("XZ")
    .center(outer_radius - keyway_depth / 2.0, (coupler_length - keyway_length) / 2.0)
    .rect(keyway_depth, keyway_length)
    .extrude(keyway_width)
)
result = result.cut(keyway)

result = result.faces(">Z").edges().chamfer(chamfer_size)

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-drill_hole_spacing / 2, 0), (drill_hole_spacing / 2, 0)])
    .hole(drill_hole_diameter)
)
