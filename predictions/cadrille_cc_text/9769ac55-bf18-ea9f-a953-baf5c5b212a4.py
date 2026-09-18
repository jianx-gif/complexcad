import cadquery as cq
outer_radius = 40.0
inner_radius = 35.0
shell_height = 10.0
rim_height = 5.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
chamfer_distance = 1.0
base = cq.Workplane('XY').circle(outer_radius).extrude(shell_height)
rim = cq.Workplane('XY').circle(inner_radius).extrude(rim_height)
rim = rim.edges().chamfer(chamfer_distance)
rim = rim.edges().fillet(inner_fillet_radius)
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
result = base.cut(hole_positions)
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.faces('>Z').edges().chamfer(chamfer_distance)
