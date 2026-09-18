import cadquery as cq

outer_diameter = 80.0
outer_diameter = 50.0
outer_diameter = 10.0
wall_thickness = 2.0
wall_thickness = 1.0
wall_thickness = 2.0
hole_diameter = 2.0
hole_count = 15
hole_count = 20
hole_count = 20
hole_count = 20
hole_count = 15
hole_count = 20
hole_spacing = 20
hole_spacing = 20
hole_spacing = 20

base = cq.Workplane('XY').box(outer_diameter, outer_length, outer_height, outer_height)
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces('>Z').workplane().hole(hole_diameter)
solid = solid.edges("|Z').fillet(outer_diameter)
solid = solid.edges("|Z').workplane().hole(hole_diameter)
solid = solid.edges("|Z').fillet(outer_diameter)
solid = solid.edges("|Z').workplane().pushPoints(hole_spacing, 0).hole(hole_diameter)
solid = solid.edges("|Z').workplane().pushPoints(hole_spacing, 0).rect(outer_diameter, outer_diameter)
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.edges().translate((0, 0), (0, 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), 0, 0