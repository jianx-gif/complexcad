import cadquery as cq
outer_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
base = base.cut(inner)
base = base.edges().fillet(inner_radius)
base = base.faces('>Z').workplane().hole(inner_radius * 2)
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-wall_thickness)
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-wall_thickness)
base = base.faces('>Z').workplane().circle(inner_radius).cutBlind(-wall_thickness).translate((0,0,0))
base = base.faces('>Z').workplane().polarArray(radius=inner_radius - wall_thickness/2, startAngle=0, angle=360, count=inner_radius).rect(inner_radius, inner_radius).cutBlind(-inner_radius)
base = base.faces('<Z').workplane().polarArray(radius=inner_radius - wall_thickness/2, count=inner_radius, startAngle=0, angle=360).rect(inner_radius, inner_radius).cutBlind(-inner_radius)
base = base.faces('>Z').workplane().pushPoints([(-inner_radius/2, 0), (inner_radius/2, 0)]).hole(inner_radius*2, inner_radius)
base = base.faces('<Z').workplane().pushPoints([(-inner_radius/2, 0), (inner_radius/2, 0)]).hole(inner_radius*2, inner_radius)
base = base.faces('<Z').workplane().pushPoints([(-inner_radius/2, 0), (inner_radius/2, 0)]).hole(inner_radius*2, inner_radius)
result = base
