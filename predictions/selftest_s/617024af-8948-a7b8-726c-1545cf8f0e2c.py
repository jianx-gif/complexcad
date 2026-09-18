import cadquery as cq

leg_length_long = 80.0
leg_length_short = 50.0
leg_width = 20.0
leg_thickness = 10.0
outer = cq.Workplane('XY').rect(leg_length_long + leg_width, leg_length_short + leg_width).extrude(leg_thickness)
cutout = cq.Workplane('XY').rect(leg_width, leg_width).extrude(leg_thickness)
l_bracket = outer.cut(cutout)
result = l_bracket
