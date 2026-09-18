import cadquery as cq
body_width = 80.0
body_height = 40.0
body_thickness = 12.0
wall_thickness = 2.0
vent_hole_dia = 4.0
vent_spacing_x = 12.0
vent_spacing_y = 12.0
vent_rows = 2
vent_cols = 3
vent_rows = 2
vent_rows = 2
vent_hole_radius = (body_width - 2 * wall_thickness) / 2
vent_hole_radius = (body_height - 2 * wall_thickness) / 2
vent_hole_radius = (vent_rows - 2 * wall_thickness) / 2
vent_hole_radius = (vent_rows - 2 * wall_thickness) / 2
body = (
    cq.Workplane("XY")
    .rect(body_width, body_height)
    .extrude(body_thickness)
)
body = body.faces(">Z").workplane().circle(vent_hole_radius).extrude(vent_hole_radius)
body = body.faces(">Z").workplane().circle(vent_hole_radius).cutBlind(-body_thickness)
body = body.faces("<Z").workplane().circle(vent_hole_radius).extrude(vent_hole_radius)
body = body.faces("<Z").workplane().circle(vent_hole_radius).extrude(vent_rows).translate((0, 0, body_thickness))
body = body.faces("<Z").workplane().rect(vent_cols, vent_rows).extrude(vent_hole_radius).translate((vent_rows - vent_spacing_x, vent_spacing_y, body_thickness - vent_rows)).extrude(vent_hole_radius).translate((vent_rows - vent_rows, vent_rows - vent_rows)).rect(vent_rows, vent_rows).extrude(vent_hole_radius).translate((vent_rows - vent_rows, vent_rows - vent_rows, body_thickness - vent_rows)).extrude(vent_hole_radius).translate((vent_rows - vent_rows, vent_rows - vent_rows, body_thickness - vent_rows)).translate((0, 0, body_thickness - vent_rows)).translate((0, 0, body_thickness - vent_rows)).translate((0, 0, body_thickness - vent_rows)).translate((0, 0, body_thickness - vent_rows)).translate((0, 0, body_thickness - vent_rows)))
body = body.edges("|Z").chamfer(chamfer_dist)
result = body
