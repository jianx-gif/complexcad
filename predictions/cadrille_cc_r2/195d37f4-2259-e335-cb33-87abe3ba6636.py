import cadquery as cq
import math
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base = cq.Workplane('XY').circle(outer_radius).extrude(base)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base)
result = base.cut(inner)
