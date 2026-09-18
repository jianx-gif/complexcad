import cadquery as cq

outer_radius = 80.0
outer_radius = 20.0
outer_radius = 1.0
outer_radius = outer_radius - 1.0
outer_radius = outer_radius - 1.0
outer_radius = outer_radius - 1.0
outer_radius = outer_radius + outer_radius + outer_radius) / 2.0
hole_count = outer_radius + outer_radius + outer_radius) / 2.0
hole_count = outer_radius + outer_radius + outer_height
hole_count = outer_radius + outer_height
hole_count = outer_radius + outer_height
hole_count = outer_height
hole_count = outer_height
hole_count = outer_height
hole_count = outer_height - hole_count
hole_count = outer_height - hole_depth)
hole = (
    cq.Workplane('XY')
    .box(outer_radius, outer_height, handle_height)
    .faces('>Z').workplane().rect(outer_radius, outer_height).cutBlind(-outer_radius)
)

hole = (
    cq.Workplane('XY')
    .box(outer_radius, outer_height, handle_height)
    .translate((outer_radius, outer_height + 0.5)
    .rect(outer_radius, outer_height)
    .extrude(-outer_height)
)
    .translate((outer_radius, outer_height + 0.8)
    .rect(outer_radius, outer_height)
    .extrude(outer_height)
    .translate((outer_radius, outer_height + 0.8)
    .extrude(outer_height)
)
)

hole = (
    cq.Workplane('XY')
    .box(outer_radius, outer_height, handle_height)
    .translate((outer_radius, outer_height + 0.8)
    .rect(outer_radius, outer_height)
    .extrude(outer_height)
    .translate((outer_radius, outer_height + 0.8)
)
)
