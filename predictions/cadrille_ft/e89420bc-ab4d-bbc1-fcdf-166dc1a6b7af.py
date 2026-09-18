import cadquery as cq

outer_radius = 80.0
outer_radius = 20.0
wall_thickness = 4.0
wall_thickness = 1.0
wall_thickness = 2.0
wall_thickness = 1.0
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5
wall_thickness = 0.5

wall_thickness = 0.5

wall_thickness = 0.5

wall_thickness = 0.5

wall_thickness = 0.5
wall_thickness = 0.5

wall_thickness = cq.Workplane('XY').circle(outer_radius).circle(outer_radius).extrude(-wall_thickness)
result = cq.Workplane('XY').circle(outer_radius).extrude(-wall_thickness)
result = result.faces('>Z').translate((0, 0, 0), (0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), (0, 0, 0), (0, 0, -wall_thickness))
result = result.faces('>Z').translate((0, 0, -wall_thickness/2))
