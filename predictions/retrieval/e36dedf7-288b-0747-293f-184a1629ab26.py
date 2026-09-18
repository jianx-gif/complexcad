import cadquery as cq
import math
outer_diameter = 80.0
height = 30.0
bore_diameter = 30.0
lip_thickness = 8.0
lip_height = 6.0
lip_chamfer = 1.0
rib_count = 12
rib_width = 3.0
rib_thickness = 4.0
rib_margin = 4.0
# rib_length computed later
# base cylinder
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(height)
# central bore through entire part
base = base.faces('>Z').workplane().hole(bore_diameter)
# compute rib length from bore to outer wall minus margins
rib_length = (outer_diameter - bore_diameter)/2 - rib_margin
rib_center_radius = bore_diameter/2 + rib_margin + rib_length/2
# create ribs on bottom face
points = [(rib_center_radius*math.cos(2*math.pi*i/rib_count), rib_center_radius*math.sin(2*math.pi*i/rib_count)) for i in range(rib_count)]
ribs = (cq.Workplane('XY')
        .pushPoints(points)
        .rect(rib_width, rib_length)
        .extrude(rib_thickness))
# create outer lip as a ring on top
outer_lip = (cq.Workplane('XY')
            .circle(outer_diameter/2 + lip_thickness)
            .extrude(lip_height)
            .faces('>Z')
            .workplane()
            .circle(outer_diameter/2)
            .cutBlind(-lip_height))
# combine features
result = base.union(ribs).union(outer_lip)
# chamfer outer lip outer edge (top outer circular edge)
result = result.faces('>Z').edges().chamfer(lip_chamfer)
