import cadquery as cq
import math
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
height = 12.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_count = 4
hole_offset = 10.0
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
base = base.cut(inner)
base = base.edges('|Z').fillet(fillet_radius)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().circle(hole_diameter/2).cutBlind(-hole_depth)
base = base.faces('>Z').workplane().circle(hole_diameter/2).cutBlind(-hole_depth)
base = base.faces('>Z').workplane().circle(hole_diameter/2).cutBlind(-hole_depth)
base = base.faces('>Z').workplane().circle(hole_diameter/2).cutBlind(-hole_depth)
base = base.faces('>Z').workplane().circle(hole_diameter/2).cutBlind(-hole_depth).translate((0,0,height/2 - hole_offset, 0))
base = base.union(base)
result = base
