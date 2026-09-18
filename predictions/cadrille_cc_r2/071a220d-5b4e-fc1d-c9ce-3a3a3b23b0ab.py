import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 80
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
result = inner.union(inner)
