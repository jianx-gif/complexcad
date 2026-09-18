import cadquery as cq
outer_diameter = 30.0
inner_diameter = 20.0
wall_thickness = 2.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius + wall_thickness
base = cq.Workplane('XY').circle(outer_diameter / 2.0).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, base_thickness))
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, base_thickness))
result = base.cut(inner)
