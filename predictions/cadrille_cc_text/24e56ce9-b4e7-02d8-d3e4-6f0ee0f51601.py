import cadquery as cq
body_height = 80.0
body_radius = 30.0
body_height = 50.0
body_radius = 20.0
body_height = body_height - 2 * seat_start_height
body_tip_radius = 20.0
body_tip_height = 80.0
bolt_radius = 8.0
bolt_hole_radius = 40.0
bolt_hole_count = 6
bolt_hole_radius = 30.0
bolt_pattern_radius = 30.0
bolt_pattern_count = 4
bolt_hole_radius = 30.0
flange_radius = 40.0
flange_thickness = 10.0
body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(body_radius, 0)
    .lineTo(body_radius, body_height - flange_thickness)
    .lineTo(body_radius + flange_radius, body_height - flange_thickness)
    .lineTo(body_radius + flange_radius, body_height)
    .lineTo(body_radius, body_height)
    .close()
    .revolve()
)
body = body.faces(">Z").edges().fillet(bolt_hole_radius)
body = body.faces(">Z").workplane().circle(bolt_hole_radius).cutBlind(-body_height)
body = body.faces(">Z").workplane().circle(bolt_hole_radius).extrude(bolt_pattern_radius)
body = body.faces(">Z").workplane().polarArray(radius=bolt_hole_radius, count=bolt_hole_count, angle=360).hole(bolt_hole_radius)
body = body.faces(">Z").workplane().polarArray(radius=bolt_hole_radius, count=bolt_hole_count, hole_hole_radius).hole(bolt_hole_radius)
body = body.faces(">Z").edges().fillet(bolt_hole_radius)
body = body.faces("<Z").edges().chamfer(bolt_hole_radius)
body = body.faces("<Z").edges().fillet(bolt_hole_radius)
body = body.faces("<Z").edges().chamfer(bolt_hole_radius)
body = body.faces("<Z").edges().fillet(bolt_hole_radius)
result = body
