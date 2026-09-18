import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 40.0
housing_length = 30.0
flange_thickness = 6.0
flange_diameter = 100.0
keyway_width = 6.0
keyway_depth = 4.0
keyway_length = 20.0
knurl_pitch = 5.0
knurl_width = 2.0
knurl_depth = 1.0
knurl_rows = 4
knurl_cols = 8
chamfer_size = 0.8

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
flange_radius = flange_diameter / 2.0
knurl_start_z = (housing_length - (knurl_rows - 1) * knurl_pitch) / 2.0

# Base housing profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, housing_length)
    .lineTo(flange_radius, housing_length)
    .lineTo(flange_radius, housing_length + flange_thickness)
    .lineTo(inner_radius, housing_length + flange_thickness)
    .close()
)

housing = profile.revolve()

# Keyway cut (rectangular slot on inner bore)
keyway = (
    cq.Workplane("XY")
    .box(keyway_width, keyway_length, keyway_depth)
    .translate((inner_radius - keyway_depth / 2.0, 0, housing_length / 2.0))
)

housing = housing.cut(keyway)

# Knurl pattern on outer cylindrical surface
knurl = cq.Workplane("XY")
for i in range(knurl_rows):
    z_pos = knurl_start_z + i * knurl_pitch
    for j in range(knurl_cols):
        angle = j * 360.0 / knurl_cols
        knurl_piece = (
            cq.Workplane("XY")
            .box(knurl_width, knurl_depth, knurl_width)
            .rotate((0, 0, 0), (0, 0, 1), angle)
            .translate((outer_radius - knurl_depth / 2.0, 0, z_pos))
        )
        knurl = knurl.union(knurl_piece)

housing = housing.cut(knurl)

# Chamfer outer edges for safety
housing = housing.edges("|Z").chamfer(chamfer_size)

result = housing