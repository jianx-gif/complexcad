import cadquery as cq
import math
circle_radius = 20.0
loft_height = 60.0
wall_thickness = 2.0
rib_width = 8.0
rib_thickness = 3.0
rib_spacing = 20.0
rib_count = 4
chamfer_size = 0.5
fillet_radius = 1.5
base = cq.Workplane('XY').circle(circle_radius).extrude(loft_height)
base = base.edges().fillet(fillet_radius)
base = base.faces('>Z').workplane().rect(rib_thickness, rib_width).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_thickness, rib_width).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_thickness, rib_width).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_thickness, rib_width).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_thickness, rib_width).extrude(rib_thickness).translate((0, 0, wall_thickness))
base = base.union(base)
base = base.faces('>Z').edges().chamfer(chamfer_size)
rib = cq.Workplane('XY').rect(rib_thickness, rib_width).extrude(rib_thickness)
rib = rib.translate((0, 0, wall_thickness))
result = base.union(rib)
