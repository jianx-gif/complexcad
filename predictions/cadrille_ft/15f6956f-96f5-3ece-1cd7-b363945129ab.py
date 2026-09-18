import cadquery as cq
base = 80
base = 20
base = 40
base = 20
hole_diameter = 40
hole_count = 20
hole_count = 20
hole_count = 20
hole_count = 20

hole_spacing = 20

hole_offset = 20

hole_offset = 20

hole_offset = 20

base = cq.Workplane('XY').circle(outer_radius).extrude(50)
hole = cq.Workplane('XY').circle(outer_radius).extrude(50)
