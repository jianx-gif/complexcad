import cadquery as cq
housing_length = 80.0
outer_radius = 30.0
wall_thickness = 3.0
shaft_radius = 8.0
shaft_radius = shaft_recess_depth
rib_thickness = 2.0
rib_width = 6.0
rib_height = outer_radius - wall_thickness
rib_count = 12
rib_count = 24
chamfer_size = 0.8
base = cq.Workplane('XY').cylinder(housing_length, outer_radius)
shell = base.shell(-wall_thickness)
shaft = (
    cq.Workplane('XY')
    .cylinder(shaft_radius, outer_radius - wall_thickness)
    .translate((0, 0, wall_thickness))
)
shell = shell.cut(shaft)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .translate((0, 0, wall_thickness))
)
shell = shell.union(rib)
shell = shell.edges().chamfer(chamfer_size)
shell = shell.faces('>Z').workplane().rarray(0, 0, 2, 1).rect(rib_width, rib_thickness).cutBlind(-rib_height)
shell = shell.faces('>Z').edges().chamfer(chamfer_size)
shell = shell.faces('>Z').workplane().rarray(0, 0, 2, 1).rect(rib_width, rib_thickness).cutBlind(-rib_height)
shell = shell.faces('>Z').edges().chamfer(chamfer_size)
result = shell
