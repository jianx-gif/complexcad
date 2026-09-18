import cadquery as cq

outer_radius = 45.0
inner_radius = 30.0
cap_height = 60.0
shoulder_height = 10.0
through_hole_diameter = 20.0
fillet_radius = 2.0
chamfer_size = 1.0
knurl_width = 5.0
knurl_depth = 2.0
knurl_height = 2.0
knurl_count = 30

wp = cq.Workplane('XY')
profile = (wp.moveTo(0, 0)
           .lineTo(outer_radius, 0)
           .lineTo(outer_radius, cap_height - shoulder_height)
           .lineTo(inner_radius, cap_height)
           .lineTo(0, cap_height)
           .close())
result = profile.revolve()
central_cyl = cq.Workplane('XY').circle(through_hole_diameter / 2).extrude(cap_height * 1.2)
result = result.cut(central_cyl)
result = result.edges('|Z').fillet(fillet_radius)
result = result.edges('>Z').chamfer(chamfer_size)
knurl = (cq.Workplane('XY')
         .workplane(offset=cap_height/2)
         .polarArray(radius=outer_radius - knurl_depth/2, count=knurl_count, startAngle=0, angle=360)
         .box(knurl_width, knurl_depth, knurl_height, centered=True))
result = result.cut(knurl)
