import cadquery as cq

shaft_diameter = 20.0
collar_height = 30.0
outer_diameter = 40.0
shoulder_height = 8.0
set_screw_diameter = 5.0
set_screw_depth = 12.0
pocket_width = 6.0
pocket_depth = 4.0
chamfer_distance = 1.0

inner_radius = shaft_diameter / 2.0
outer_radius = outer_diameter / 2.0
shoulder_start = collar_height - shoulder_height
wall_thickness = outer_radius - inner_radius

solid = (
    cq.Workplane("XY")
    .lineTo(0, collar_height)
    .lineTo(outer_radius, collar_height)
    .lineTo(outer_radius, shoulder_start)
    .lineTo(inner_radius, shoulder_start)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)

# milled shoulder pocket (rectangular slot) cut radially
pocket = (
    cq.Workplane("XY")
    .box(pocket_width, pocket_depth, wall_thickness - 1.0)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((outer_radius, 0, shoulder_start + shoulder_height / 2))
)
solid = solid.cut(pocket)

# blind set screw hole (radial cylinder)
set_screw = (
    cq.Workplane("XY")
    .cylinder(set_screw_depth, set_screw_diameter)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((outer_radius, 0, shoulder_start + shoulder_height / 4))
)
solid = solid.cut(set_screw)

result = solid.edges().chamfer(chamfer_distance)
