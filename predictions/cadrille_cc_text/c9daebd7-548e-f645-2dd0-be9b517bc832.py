import cadquery as cq
outer_radius = 40.0
length = 80.0
wall_thickness = 5.0
tab_width = 30.0
tab_height = 15.0
tab_thickness = 8.0
clearance_hole_dia = 3.0
tab_hole_dia = 6.0
tab_thickness = 8.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(length)
inner_cyl = cq.Workplane('XY').circle(outer_radius).extrude(length)
tab = cq.Workplane('XY').rect(tab_thickness, tab_height).extrude(length)
tab = tab.translate((0, 0, wall_thickness))
tab = tab.translate((0, 0, wall_thickness))
tab = tab.translate((0, 0, wall_thickness))
result = outer_cyl.union(tab)
result = result.faces('>Z').edges().fillet(outer_cyl)
result = result.faces('>Z').workplane().hole(clearance_hole_dia)
result = result.faces('>Z').workplane().polarArray(radius=outer_radius - wall_thickness/2, count=4, startAngle=0, angle=360).hole(clearance_hole_dia)
