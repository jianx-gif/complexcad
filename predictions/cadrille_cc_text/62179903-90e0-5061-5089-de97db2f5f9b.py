import cadquery as cq
knob_diameter = 60.0
knob_height = 30.0
wall_thickness = 2.0
central_hole_diameter = 12.0
groove_width = 8.0
groove_depth = 3.0
chamfer_distance = 1.0
tab_thickness = 4.0
tab_width = 20.0
tab_length = 10.0
tab_thickness = wall_thickness
base = cq.Workplane('XY').circle(knob_diameter/2).extrude(knob_height)
base = base.faces('>Z').workplane().circle(central_hole_diameter/2).cutBlind(-knob_height)
base = base.faces('>Z').workplane().circle(central_hole_diameter/2).cutBlind(-knob_height)
base = base.faces('>Z').workplane().polarArray(radius=knob_diameter/2, count=knob_diameter/2, startAngle=0, angle=360).rect(tab_thickness, tab_width).cutBlind(-tab_thickness)
base = base.faces('>Z').workplane().circle(central_hole_diameter/2).cutBlind(-tab_thickness)
base = base.faces('>Z').workplane().polarArray(radius=central_hole_diameter/2, count=tab_thickness, startAngle=0, angle=360).rect(tab_thickness, tab_width).cutBlind(-tab_thickness)
base = base.faces('>Z').workplane().polarArray(radius=central_hole_diameter/2, count=tab_thickness, startAngle=0, angle=360).rect(tab_thickness, tab_width).extrude(tab_thickness)
base = base.union(base)
base = base.faces('>Z').workplane().circle(central_hole_diameter/2).cutBlind(-central_hole_depth)
result = base
