import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
body_height = 60.0
notch_width = 5.0
notch_height = 20.0

wp = cq.Workplane('XZ')
profile = (
    wp.moveTo(inner_radius,0)
      .lineTo(outer_radius,0)
      .threePointArc((outer_radius+5, body_height/2),(outer_radius, body_height))
      .lineTo(inner_radius, body_height)
      .threePointArc((inner_radius-5, body_height/2),(inner_radius,0))
      .close()
)
body = profile.revolve()
notch = (
    cq.Workplane('XZ')
    .center(outer_radius, body_height/2)
    .rect(notch_width, notch_height)
    .extrude(- (outer_radius - inner_radius) )
)
body = body.cut(notch)
result = body
