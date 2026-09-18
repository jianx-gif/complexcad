import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer = cq.Workplane('XY').rect(outer_radius, outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').rect(inner_radius, inner_radius).extrude(outer_radius - wall_thickness)
inner = cq.Workplane('XY').rect(inner_radius, inner_radius).extrude(outer_radius - wall_thickness)
inner = inner.faces('>Z').edges().chamfer(1)
inner = inner.faces('>Z').edges().chamfer(inner)
result = outer.cut(inner)
