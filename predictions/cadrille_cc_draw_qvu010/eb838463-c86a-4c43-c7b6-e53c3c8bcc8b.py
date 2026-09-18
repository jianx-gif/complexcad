import cadquery as cq
import math
outer_diameter = 100.0
inner_diameter = 30.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 1.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
inner_cyl = cq.Workplane('XY').circle(inner_diameter/2).extrude(thickness)
rib = base.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_width)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_width)
rib = rib.translate((outer_diameter/2 - rib_width/2, 0, 0))
rib = rib.translate((outer_diameter/2 - rib_width/2, 0, 0))
rib = rib.translate((outer_diameter/2 - rib_width/2, 0, 0))
rib = rib.translate((outer_diameter/2 - rib_width/2, 0, 0))
combined = rib.union(rib)
combined = combined.faces('>Z').workplane().pushPoints([(0, 0), (0, 1)]).hole(inner_diameter)
combined = combined.faces('>Z').workplane().pushPoints([(0, 0), (0, 1), -0.1).hole(inner_diameter)
result = combined
