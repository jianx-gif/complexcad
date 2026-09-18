import cadquery as cq
leg_length_long = 80.0
leg_length_short = 50.0
leg_thickness = 10.0
leg_width = 20.0
base = cq.Workplane('XY').rect(leg_length_long, leg_width).extrude(leg_thickness)
base = base.edges('|Z').chamfer(leg_width)
base = base.faces('>Z').workplane().rect(leg_width, leg_length_short).cutBlind(-leg_thickness)
base = base.faces('>Z').workplane().rect(leg_width, leg_length_short).cutBlind(-leg_thickness)
base = base.faces('>Z').workplane().center(leg_width/2 - leg_width/2, leg_length_short/2).rect(leg_width, leg_length_short).extrude(leg_thickness)
base = base.faces('>Z').workplane().center(leg_width/2 - leg_width/2, leg_length_short/2).rect(leg_width, leg_length_short).extrude(leg_thickness).translate((leg_width/2, leg_length_short/2, leg_thickness)))
base = base.edges('>Z').chamfer(leg_width/2)
result = base
