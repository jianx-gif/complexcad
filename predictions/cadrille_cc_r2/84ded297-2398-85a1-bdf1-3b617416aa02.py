import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_distance = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
inner_radius = outer_diameter/2 - inner_diameter/2
inner_radius = inner_radius + inner_radius
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-thickness)
base = base.edges('|Z').chamfer(chamfer_size)
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-thickness)
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-thickness)
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-thickness).cutBlind(-thickness).translate((0, 0, thickness))
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-thickness).cutBlind(-thickness).translate((0, 0, thickness))
base = base.faces('>Z').workplane().circle(hole_diameter/2).cutBlind(-thickness).cutBlind(-thickness)
base = base.faces('>Z').workplane().polarArray(hole_spacing, 0, 3, 4).hole(hole_diameter)
result = base
