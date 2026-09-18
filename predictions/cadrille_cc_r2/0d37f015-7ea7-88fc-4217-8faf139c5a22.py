import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
fillet_radius = 2.0
chamfer_distance = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, wall_thickness))
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, wall_thickness))
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, wall_thickness))
result = outer.cut(inner)
