import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 20.0
height = 60.0
wall_thickness = outer_radius - inner_radius
chamfer_size = 2.0
rib_thickness = 2.0
rib_height = 40.0
rib_offset = 5.0
hole_diameter = 5.0
hole_depth = 15.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height - wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(0, wall_thickness)
    .close()
)

# Revolve to create housing
housing = profile.revolve()

# Chamfer outer rim edges (top and bottom)
housing = housing.faces(">Z").edges().chamfer(chamfer_size)
housing = housing.faces("<Z").edges().chamfer(chamfer_size)

# Internal rib (cylindrical boss) positioned inside cavity
rib = (
    cq.Workplane("XY")
    .circle(inner_radius - rib_thickness)
    .extrude(rib_height)
    .translate((0, 0, rib_offset))
)

housing = housing.union(rib)

# Blind holes pattern on top face
hole_positions = []
start_x = -((hole_cols - 1) * hole_spacing) / 2
start_y = -((hole_rows - 1) * hole_spacing) / 2
for i in range(hole_cols):
    for j in range(hole_rows):
        hole_positions.append((start_x + i * hole_spacing, start_y + j * hole_spacing))

housing = (
    housing.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)

result = housing