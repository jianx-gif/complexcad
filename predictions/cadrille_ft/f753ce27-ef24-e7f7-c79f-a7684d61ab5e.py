import cadquery as cq

outer_diameter = 80.0
outer_diameter = 30.0
wall_thickness = 10.0
wall_thickness = 2.0
chamfer_distance = 1.0
chamfer_distance = 1.0
chamfer_distance = 1.0
chamfer_distance = 0.5

chamfer_distance = 0.5

chamfer_distance = 0.5

chamfer_distance = 0.5

chamfer_distance = 0.5

chamfer_distance = 0.5

cylinder = cq.Workplane('XY').cylinder(cylinder = outer_diameter/2).translate((0, 0, 0), (0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, -outer_diameter)
result = cq.Workplane('XY').box(outer_diameter, outer_diameter, outer_diameter)
result = cq.Workplane('XY').box(outer_diameter, outer_dthickness, outer_diameter)
result = result.faces('>Z').edges().chamfer(chamfer_distance)
