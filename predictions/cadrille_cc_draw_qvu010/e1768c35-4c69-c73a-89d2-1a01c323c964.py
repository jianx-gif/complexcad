import cadquery as cq
import math
outer_radius = 20.0
inner_radius = 15.0
thickness = 5.0
rib_height = 12.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(thickness)
rib = outer.cut(inner)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(thickness)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(thickness)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(thickness)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(thickness)
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
result = rib
