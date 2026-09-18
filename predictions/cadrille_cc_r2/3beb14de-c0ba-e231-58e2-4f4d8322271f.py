import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
height = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
result = base.cut(inner)
