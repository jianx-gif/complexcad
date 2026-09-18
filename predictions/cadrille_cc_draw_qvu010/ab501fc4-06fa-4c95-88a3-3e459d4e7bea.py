import cadquery as cq
import math
outer_diameter = 80.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
rib_width = 5.0
rib_height = 3.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
base = cq.Workplane('XY').circle(outer_diameter / 2).extrude(wall_thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
rib = base.cut(inner_cyl)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
result = rib
