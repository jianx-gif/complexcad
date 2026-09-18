import cadquery as cq
body_length = 60.0
body_radius = 12.0
inlet_radius = 6.0
flange_radius = 30.0
flange_thickness = 8.0
mount_hole_dia = 8.0
mount_hole_radius = 20.0
mount_hole_count = 4
mount_hole_radius = mount_hole_dia / 2
body = (
    cq.Workplane("XZ")
    .moveTo(body_radius, 0)
    .lineTo(body_radius, body_length)
    .lineTo(inlet_radius, body_length)
    .lineTo(inlet_radius, 0)
    .close()
    .revolve()
)
body = body.faces(">Z").workplane().hole(inlet_radius * 2)
body = body.edges().fillet(fillet_radius)
body = (
    body.faces(">Z").workplane()
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_dia)
)
body = (
    body.faces(">Z").workplane()
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_dia)
)
result = body
