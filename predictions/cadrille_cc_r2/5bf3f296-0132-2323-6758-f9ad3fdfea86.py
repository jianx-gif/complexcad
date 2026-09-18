import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base_height = 10.0
base_fillet = 0.5
chamfer_distance = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(base_height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_height)
inner = inner.cut(inner)
result = inner
