import cadquery as cq
outer_radius = 15.0
inner_radius = 15.0
inner_radius = outer_radius - inner_radius
shoulder_height = 60.0
shoulder_radius = 20.0
shoulder_height = 10.0
shoulder_radius = 30.0
shoulder_height = 8.0
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, shoulder_height)
    .lineTo(inner_radius, shoulder_height)
    .lineTo(inner_radius, shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height + shoulder_height)
    .lineTo(outer_radius, shoulder_height + shoulder_height + shoulder_height)
    .lineTo(0, shoulder_height + shoulder_height + shoulder_height)
    .close()
)
result = (
    profile
    .revolve()
    .edges()
    .chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)
