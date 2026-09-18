import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
outer_radius = outer_diameter/2
inner_radius = inner_diameter/2
base = cq.Workplane('XY').circle(outer_radius).circle(inner_radius).extrude(thickness)
result = base.faces('>Z').workplane().polarArray(radius=(inner_radius+outer_radius)/2, count=6, startAngle=0, angle=360).hole(4)
