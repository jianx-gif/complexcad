import cadquery as cq
body_diameter = 80.0
body_height = 60.0
wall_thickness = 5.0
groove_width = 2.0
groove_depth = 4.0
groove_thickness = 4.0
vent_hole_diameter = 8.0
vent_hole_offset_z = 30.0
fillet_radius = 0.5
bore_diameter = 30.0
lug_height = 6.0
lug_width = 12.0
lug_thickness = 4.0
vent_hole_offset_z = 30.0
body = cq.Workplane('XY').circle(body_diameter / 2).extrude(body_height)
body = body.faces('>Z').workplane().hole(bore_diameter)
body = body.faces('>Z').workplane().circle(bore_diameter / 2).extrude(body_height)
body = body.faces('>Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness, count=vent_hole_offset_z, startAngle=0, angle=360).hole(vent_hole_diameter)
body = body.faces('>Z').workplane().circle(bore_diameter / 2).extrude(body_height + 2)
body = body.faces('>Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - groove_width, count=vent_hole_offset_z, angle=360).circle(groove_diameter / 2).cutBlind(groove_depth)
body = body.faces('>Z').workplane().circle(bore_diameter / 2).extrude(body_height + 2)
body = body.faces('<Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - groove_width, count=vent_hole_offset_z, angle=360).circle(vent_hole_diameter / 2).extrude(body_height + 2)
body = body.faces('<Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - groove_width - 10).circle(groove_diameter / 2).extrude(body_height + 2)
body = body.edges().fillet(fillet_radius)
body = body.faces('>Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - 10).circle(bore_diameter / 2).extrude(bore_depth)
body = body.edges().fillet(fillet_radius)
body = body.faces('<Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - 10).circle(vent_hole_diameter / 2).extrude(body_height + 2)
body = body.faces('<Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - 10).circle(vent_hole_diameter / 2).extrude(body_height + 2)
body = body.faces('<Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - 10).circle(vent_hole_diameter / 2).extrude(body_height + 2)
body = body.faces('<Z').workplane().polarArray(radius=body_diameter / 2 - wall_thickness - 10).circle(vent_hole_diameter / 2).extrude(body_height + 2)
body = body.faces('<Z').edges().fillet(fillet_radius)
body = body.edges().chamfer(body)
body = body.faces('>Z').edges().fillet(fillet_radius)
body = body.faces('>Z').edges().chamfer(body=body.translate((body_diameter / 2 - wall_thickness - groove_width - 0.01, 0, body_height / 2))
body = body.faces('>Z').workplane().pushPoints([(0,0)])
body = body.faces('<Z').workplane().pushPoints([(body_diameter / 2 - wall_thickness - 10, body_height / 2 - 10)).hole(vent_hole_diameter)
result = body
