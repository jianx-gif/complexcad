import cadquery as cq
outer_radius = 45
inner_radius = 30
wall_thickness = 5
inner_radius = inner_radius - wall_thickness
chamfer_distance = 1
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
result = outer.cut(inner)
