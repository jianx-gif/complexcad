import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 1.0
wall_thickness = 2.0
chamfer_distance = 1.0
chamfer_distance = 0.5
hole_diameter = 2.0
hole_count = 15
hole_count = 15
hole_count = 15
hole_count = 20
hole_count = 15
hole_count = 20
hole_spacing = 20

hole_spacing = 20

base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
outer = outer.cut(inner)
outer = outer.edges('>Z').workplane().circle((outer_radius - outer_radius)
outer = outer.edges('>Z').chamfer(chamfer_distance)
