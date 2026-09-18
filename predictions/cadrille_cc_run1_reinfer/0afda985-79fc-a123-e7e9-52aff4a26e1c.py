import cadquery as cq
outer_diameter = 30.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius + wall_thickness
base = cq.Workplane('XY').circle(outer_diameter / 2.0).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = inner.union(inner)
inner = inner.edges('|Z').fillet(inner_radius)
inner = inner.faces('>Z').workplane().hole(inner_diameter)
inner = inner.faces('>Z').workplane().circle(inner_radius).cutBlind(-inner_radius)
result = inner
