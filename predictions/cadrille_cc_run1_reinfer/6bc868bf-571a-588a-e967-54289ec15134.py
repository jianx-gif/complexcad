import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = cq.Workplane('XY').circle(outer_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = inner.union(inner)
inner = inner.edges().fillet(inner_radius)
inner = inner.faces('>Z').workplane().hole(inner_radius * 2)
result = inner
