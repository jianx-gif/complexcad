import cadquery as cq

outer_radius = 30.0
wall_thickness = 4.0
inner_radius = outer_radius - wall_thickness
height = 60.0
base_fillet_radius = 2.5
tab_width = 20.0
tab_height = 10.0
tab_thickness = 6.0
tab_hole_diameter = 4.0
tab_hole_spacing = 12.0

outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
shell = outer_cyl.cut(inner_cyl)

tab = (
    cq.Workplane('YZ')
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
    .translate((outer_radius - tab_thickness/2, 0, 0))
)

tab = (
    tab.faces('>X')
    .workplane()
    .pushPoints([(-tab_hole_spacing/2, 0), (tab_hole_spacing/2, 0)])
    .hole(tab_hole_diameter)
)

result = shell.union(tab)
result = result.faces('<Z').edges().fillet(base_fillet_radius)
