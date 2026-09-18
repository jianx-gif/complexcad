import cadquery as cq
outer_diameter = 40.0
inner_diameter = 20.0
shoulder_diameter = 30.0
shoulder_length = 70.0
shoulder_length = 15.0
blind_hole_diameter = 6.0
blind_hole_depth = 8.0
blind_hole_spacing = 8.0
blind_hole_count = 4
chamfer_size = 1.0
tab_width = 20.0
tab_thickness = 5.0
tab_height = 10.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, shoulder_length)
    .lineTo(inner_radius, shoulder_length)
    .lineTo(inner_radius, shoulder_length + shoulder_length)
    .lineTo(outer_radius, shoulder_length + shoulder_length)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
tab = (
    cq.Workplane("XY")
    .box(tab_width, tab_thickness, tab_height)
    .translate((outer_radius - tab_thickness / 2.0, 0, shoulder_length / 2.0))
)
solid = solid.cut(tab)
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)
solid = solid.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)
solid = solid.faces(">Z").workplane().polarArray(radius=outer_radius - tab_thickness / 2.0, count=blind_hole_count, startAngle=0, angle=360).hole(blind_hole_diameter, blind_hole_depth)
result = solid
