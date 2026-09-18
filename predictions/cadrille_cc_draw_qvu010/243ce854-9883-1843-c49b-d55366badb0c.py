import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(outer_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(outer_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(outer_cyl).translate((0,0,outer_cyl))
result = outer_cyl.cut(inner_cyl)
