import cadquery as cq
outer_radius = 80.0
outer_radius = 60.0
wall_thickness = 5.0
wall_thickness = 2.0
chamfer_distance = 1.0
chamfer_distance = 1.0
chamfer_distance = 1.0
hole_diameter = 2.0
hole_count = 10
hole_count = 20
hole_count = 15
hole_count = 15
hole_count = 15
hole_count = 20
hole_spacing = 20
hole_spacing = 20
hole_spacing = 20

hole_spacing = 20

hole_spacing = 20

hole_spacing = 20

hole_spacing = 20

hole_offset = 5.0
hole_offset = 5.0
hole_offset = 1.0
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = cq.Workplane('XY').circle(hole_diameter/2).extrude(hole_depth)
hole_hole = cq.Workplane('XY').circle(hole_offset).circle(hole_offset, 0)
result = hollow_hole.union(hole)
result = result.faces('>Z").workplane().hole(hole_offset, 0)
result = result.faces('>Z').workplane().hole(hole_offset, 0).hole(hole_offset, 0).hole(hole_offset, 0)
result = result.faces('>Z').workplane(hole_offset, 0).hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
