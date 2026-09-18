import cadquery as cq
import math
outer_diameter = 80.0
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
rib = base.cut(inner_cyl)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - rib_width/2, startAngle=0, angle=360).rect(rib_width, rib_height).extrude(thickness)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - rib_width/2, startAngle=0, angle=360).rect(rib_width, rib_height).extrude(thickness)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - rib_width/2, startAngle=0, angle=360).rect(rib_width, rib_height).extrude(thickness)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - rib_width/2, startAngle=0, angle=360).rect(rib_width, rib_height).extrude(thickness)
result = rib
