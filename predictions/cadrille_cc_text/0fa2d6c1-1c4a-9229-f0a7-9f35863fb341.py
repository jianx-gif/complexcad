import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
body_height = 60.0
notch_width = 5.0
notch_height = 20.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, body_height)
    .lineTo(inner_radius, body_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(2 * outer_radius)
solid = solid.faces(">Z").workplane().hole(notch_width)
solid = solid.faces(">Z").workplane().rect(notch_width, notch_height).cutBlind(notch_height)
solid = solid.faces(">Z").workplane().rect(notch_width, notch_height).cutBlind(notch_height)
result = solid
