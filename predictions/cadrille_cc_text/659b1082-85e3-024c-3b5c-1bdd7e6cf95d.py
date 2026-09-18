import cadquery as cq
outer_dia = 80.0
inner_dia = 40.0
wall_thk = 5.0
seat_depth = 10.0
seat_count = 6
flange_dia = 70.0
flange_thk = 4.0
keyway_width = 5.0
keyway_depth = 8.0
keyway_length = outer_dia - 2 * wall_thk
arc_offset = 5.0
mount_hole_dia = 12.0
mount_spacing = 30.0
outer_radius = outer_dia / 2.0
inner_radius = inner_dia / 2.0
body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, body)
    .lineTo(inner_radius, body)
    .lineTo(inner_radius, body)
    .close()
    .revolve()
)
body = body.cut(inner_radius)
body = body.edges().chamfer(seat_depth)
body = body.faces(">Z").workplane().hole(inner_dia)
body = body.faces(">Z").workplane().circle(flange_dia/2.0).cutBlind(flange_thk)
body = body.faces(">Z").workplane().circle(mount_hole_dia/2.0).cutBlind(mount_hole_dia/2.0)
body = body.faces(">Z").workplane().polarArray(radius=mount_spacing/2.0, count=mount_spacing, startAngle=0, angle=360).hole(mount_hole_dia)
body = body.faces(">Z").workplane().polarArray(radius=mount_spacing/2.0, startAngle=0, count=4, angle=360).hole(mount_hole_dia)
body = body.faces(">Z").workplane().polarArray(radius=mount_spacing/2.0, startAngle=0, count=4, angle=360).circle(flange_dia/2.0).extrude(flange_thk)
body = body.cut(flange_thk)
body = body.edges().chamfer(seat_depth)
body = body.faces("<Z").edges().chamfer(seat_depth)
body = body.faces(">Z").workplane().polarArray(radius=mount_spacing/2.0, startAngle=0, count=4, angle=360).circle(flange_dia/2.0).extrude(flange_thk)
body = body.faces(">Z").workplane().polarArray(radius=mount_spacing/2.0, count=4, angle=360).circle(flange_dia/2.0).extrude(flange_thk)
body = body.edges().chamfer(body)
body = body.faces("<Z").workplane().polarArray(radius=mount_spacing/2.0, count=4, angle=360).rect(flange_thk, keyway_width).extrude(flange_thk)
body = body.edges().chamfer(body)
result = body
