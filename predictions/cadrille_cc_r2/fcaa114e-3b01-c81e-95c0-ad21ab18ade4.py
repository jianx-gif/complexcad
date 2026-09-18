import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 80
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
base_thickness = 5
inner_radius = inner_radius - wall_thickness
base_height = height - 2 * wall_thickness
inner_radius = inner_radius + wall_thickness
outer = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = inner.cut(inner)
result = inner
