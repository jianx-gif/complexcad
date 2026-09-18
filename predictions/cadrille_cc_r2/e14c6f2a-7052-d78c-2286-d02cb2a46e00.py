import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
height = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, wall_thickness))
inner = inner.cut(inner)
result = inner
