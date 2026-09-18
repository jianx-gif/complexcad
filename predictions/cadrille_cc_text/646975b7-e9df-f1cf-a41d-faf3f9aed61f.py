import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
base_thickness = 5.0
base_thickness = base_thickness
groove_width = 3.0
groove_depth = 2.0
groove_depth = base_thickness + groove_width
fillet_radius = 1.0
groove_center_radius = outer_radius - wall_thickness/2
groove_center_z = base_thickness/2
groove_center_z = base_thickness/2
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_thickness)
    .lineTo(outer_radius + groove_width, base_thickness)
    .lineTo(outer_radius + groove_width, base_thickness + groove_width)
    .lineTo(outer_radius, base_thickness + groove_width)
    .lineTo(0, base_thickness + groove_width)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
groove = (
    cq.Workplane("XY")
    .box(groove_depth, groove_width, groove_width)
    .translate((outer_radius - groove_depth/2, 0, base_thickness + groove_width/2))
)
solid = solid.cut(groove)
solid = solid.edges().fillet(fillet_radius)
groove = (
    cq.Workplane("XY")
    .box(groove_depth, groove_width, groove_width)
    .translate((outer_radius - groove_depth/2, 0, base_thickness + groove_width/2))
)
solid = solid.cut(groove)
solid = solid.edges().fillet(fillet_radius)
result = solid
