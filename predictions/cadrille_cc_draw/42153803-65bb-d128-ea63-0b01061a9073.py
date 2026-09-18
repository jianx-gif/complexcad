import cadquery as cq
import math
base_length = 80.0
base_width = 40.0
base_thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_spacing = 15.0
rib_count = 4
rib_spacing = 12.0
chamfer_size = 1.0
base = cq.Workplane('XY').rect(base_length, base_width).extrude(base_thickness)
base = base.faces('>Z').workplane().hole(rib_height)
base = base.faces('>Z').workplane().rect(base_length, rib_width).extrude(rib_height)
rib = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_height)
rib = rib.edges('|Z').chamfer(chamfer_size)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_height)
result = rib
