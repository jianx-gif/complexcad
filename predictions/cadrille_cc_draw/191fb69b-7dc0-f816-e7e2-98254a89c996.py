import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 35.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(thickness)
rib = outer_cyl.cut(inner_cyl)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-thickness)
rib = rib.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_height)
result = rib
