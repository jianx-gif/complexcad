import cadquery as cq
import math
outer_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_radius = outer_radius - wall_thickness
wall_thickness = 0.5
rib_width = 4.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
rib = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
combined = outer.union(rib)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().center(0, 0).hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().center(0, 0).hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().center(0, 0).hole(inner_radius * 2)
result = combined
