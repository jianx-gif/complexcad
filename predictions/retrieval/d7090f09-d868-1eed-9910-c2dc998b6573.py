import cadquery as cq

# Parameters
cap_height = 30.0
wall_thickness = 5.0
outer_radius = 35.0
inner_radius = outer_radius - wall_thickness
aperture_diameter = 10.0
lip_height = 5.0
lip_thickness = 3.0
ridge_height = 2.0
ridge_width = 4.0
ridge_thickness = 2.0
ridge_count = 6
fillet_radius = 1.0
ridge_overlap = 0.1

# Base cap solid via revolve
base = (
    cq.Workplane("XZ")
    .polyline([
        (outer_radius, 0),
        (outer_radius, cap_height - lip_height),
        (outer_radius + lip_thickness, cap_height - lip_height),
        (outer_radius + lip_thickness, cap_height),
        (inner_radius, cap_height),
        (inner_radius, 0),
        (outer_radius, 0)
    ])
    .close()
    .revolve()
)

# Fillet all edges for safety
result = base.edges().fillet(fillet_radius)

# Central sealing aperture
result = result.faces(">Z").workplane().hole(aperture_diameter)

# Add external ridges around the cap
for i in range(ridge_count):
    angle = i * 360.0 / ridge_count
    ridge = (
        cq.Workplane("XY")
        .center(outer_radius + ridge_thickness / 2 - ridge_overlap, 0)
        .box(ridge_thickness, ridge_width, ridge_height, centered=(True, True, False))
        .translate((0, 0, cap_height / 2 - ridge_height / 2))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(ridge)
