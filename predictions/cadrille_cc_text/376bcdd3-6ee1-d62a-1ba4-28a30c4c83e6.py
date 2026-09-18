import cadquery as cq
outer_diameter = 80.0
inner_diameter = 60.0
height = 20.0
rim_thickness = 5.0
fillet_radius = 2.0
groove_width = 3.0
groove_depth = 2.0
groove_start = 15.0
groove_end = 15.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height - rim_thickness)
    .lineTo(inner_radius + rim_thickness, height - rim_thickness)
    .lineTo(inner_radius + rim_thickness, height - rim_thickness)
    .lineTo(inner_radius, height - rim_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
groove = (
    cq.Workplane("XY")
    .circle(groove_start)
    .extrude(groove_depth)
    .translate((0, 0, height))
)
solid = solid.cut(groove)
groove = (
    cq.Workplane("XY")
    .circle(groove_width / 2.0)
    .extrude(groove_depth)
    .translate((0, 0, height))
)
solid = solid.cut(groove)
groove = (
    cq.Workplane("XY")
    .circle(groove_width / 2.0)
    .extrude(groove_depth)
    .translate((0, 0, height))
)
solid = solid.cut(groove)
solid = solid.edges().fillet(fillet_radius)
result = solid
