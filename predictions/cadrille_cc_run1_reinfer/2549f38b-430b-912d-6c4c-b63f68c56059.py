import cadquery as cq
import math
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
rib_width = 5.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
rib = base.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.edges('|Z').chamfer(chamfer_size)
rib = rib.edges('>Z').fillet(inner_radius)
rib = rib.edges('>Z').fillet(inner_radius)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.edges('>Z').chamfer(chamfer_size)
result = rib
