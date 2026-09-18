import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 40.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 3.0
wall_thickness = 2.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 1.0
wall_thickness = 2.0
wall_thickness = 2.0
hole_diameter = 2.0
hole_spacing = 20
hole_spacing = 20
hole_spacing = 20
hole_spacing = 20

hole_spacing = 20

hole_spacing = 20

base = cq.Workplane('XY').box(outer_length, outer_length, outer_thickness)
result = cq.Workplane('XY').box(outer_length, outer_width, outer_height)
result = base.cut(inner)
result = result.faces('>Z').workplane().hole(hole_diameter)
result = result.faces('>Z').workplane().hole(hole_diameter)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_positions)
result = result.faces('>Z').workplane().hole(hole_diameter)
result = result.faces('>Z').workplane().hole(hole_diameter)
