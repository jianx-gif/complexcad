import cadquery as cq
import math
outer_diameter = 80.0
wall_thickness = 3.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_count = 8
hole_radius = outer_diameter / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(outer_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
result = outer_cyl.cut(inner_cyl)
