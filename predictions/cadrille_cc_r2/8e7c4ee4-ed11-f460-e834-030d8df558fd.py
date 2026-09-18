import cadquery as cq
outer_radius = 45
inner_radius = 20
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base_height = 8
inner_radius = inner_radius - wall_thickness
base_thickness = base_height
outer = cq.Workplane('XY').circle(outer_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
result = inner.union(inner)
result = result.edges().chamfer(outer)
