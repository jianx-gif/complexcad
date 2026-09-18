import cadquery as cq
import math
num_teeth = 12
gear_thickness = 8.0
web_thickness = 2.0
web_base_radius = 8.0
bore_diameter = 6.0
key_width = 2.0
key_depth = gear_thickness - 2.0
key_height = gear_thickness - 2.0
base = cq.Workplane('XY').circle(bore_diameter/2).extrude(gear_thickness)
base = base.faces('>Z').workplane().circle(bore_diameter/2).extrude(gear_thickness)
base = base.faces('>Z').workplane().circle(bore_diameter/2).extrude(bore_depth)
base = base.faces('>Z').workplane().circle(bore_diameter/2).extrude(bore_depth)
base = base.faces('>Z').workplane().polarArray(radius=web_base_radius, count=num_teeth, startAngle=0, angle=360).rect(key_width, key_depth).cutBlind(key_depth)
base = base.faces('>Z').workplane().circle(bore_diameter/2).extrude(key_depth)
base = base.faces('>Z').edges().chamfer(key_depth)
base = base.faces('>Z').edges().chamfer(key_depth)
result = base
