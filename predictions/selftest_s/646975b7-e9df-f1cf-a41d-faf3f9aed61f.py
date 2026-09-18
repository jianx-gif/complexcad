import cadquery as cq

outer_radius = 30
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base_thickness = 5
cone_height = 30
cone_taper = 4
cone_base_radius = inner_radius
cone_top_radius = cone_base_radius - cone_taper
total_height = base_thickness + cone_height
fillet_radius = 1.0

groove_width = 3.0
groove_depth = 2.0
groove_z_center = base_thickness + cone_height * 0.5

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, total_height)
    .lineTo(cone_top_radius, total_height)
    .lineTo(cone_base_radius, base_thickness)
    .lineTo(cone_base_radius, 0)
    .close()
)

result = profile.revolve()
result = result.edges().fillet(fillet_radius)

groove_box = (
    cq.Workplane("XY")
    .box(groove_width, 2 * outer_radius + 10, groove_depth)
    .translate((outer_radius - groove_width / 2, 0, groove_z_center - groove_depth / 2))
)

result = result.cut(groove_box)
