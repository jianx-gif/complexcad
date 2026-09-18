import cadquery as cq
outer_diameter = 30.0
wall_thickness = 3.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2
outer_radius = outer_diameter / 2
inner_radius = inner_radius - wall_thickness
base = cq.Workplane('XY').circle(outer_radius).extrude(base_height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(base_height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(base_height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = inner_cyl.cut(inner_cyl)
inner_cyl = inner_cyl.cut(inner_cyl)
result = inner_cyl.cut(inner_cyl)
