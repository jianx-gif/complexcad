import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 15
wall_thickness = 2
chamfer_distance = 2
hole_diameter = 5
hole_spacing = 30
hole_offset = 10
chamfer_distance = 2
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner_cylinder = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cylinder = cq.Workplane('XY').circle(inner_radius).extrude(height)
result = base.cut(inner_cylinder)
result = result.faces('>Z').workplane().hole(hole_diameter)
result = result.faces('>Z').edges().chamfer(chamfer_distance)
