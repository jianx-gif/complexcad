import cadquery as cq
outer_radius = 45
inner_radius = 20
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
chamfer_distance = 1
fillet_radius = 2
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, wall_thickness))
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0, 0, wall_thickness))
result = base.cut(inner)
