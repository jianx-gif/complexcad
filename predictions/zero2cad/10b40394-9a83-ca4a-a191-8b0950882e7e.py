import cadquery as cq

# Parameters
outer_diameter = 60.0
inner_diameter = 40.0
housing_length = 30.0
flange_thickness = 10.0
flange_diameter = 80.0
rib_count = 6
rib_width = 6.0
rib_height = 8.0
rib_fillet_radius = 2.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
chamfer_distance = 1.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
flange_radius = flange_diameter / 2.0
wall_thickness = outer_radius - inner_radius
rib_center_radius = outer_radius + rib_height / 2.0

# Base housing cylinder
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(housing_length)
)

# Flange on top of housing
flange = (
    cq.Workplane("XY", origin=(0, 0, housing_length))
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Combine base and flange
housing = base.union(flange)

# Internal bore (through entire length including flange)
inner_bore = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(housing_length + flange_thickness)
)

housing = housing.cut(inner_bore)

# Create a single rib solid positioned at 0 degrees
rib = (
    cq.Workplane("XY")
    .center(rib_center_radius, 0)
    .rect(rib_height, rib_width)
    .extrude(housing_length)
)

# Array ribs around Z axis
ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

# Add ribs to housing
housing = housing.union(ribs)

# Fillet rib roots (vertical edges where ribs meet housing)
housing = housing.edges("|Z").fillet(rib_fillet_radius)

# Add mounting holes on flange (four equally spaced)
for i in range(4):
    angle = 90.0 * i
    housing = (
        housing
        .faces(">Z")
        .workplane()
        .center(flange_radius - wall_thickness / 2.0, 0)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .hole(mount_hole_diameter)
    )

# Chamfer outer edge of flange for safety
housing = housing.edges("|Z").chamfer(chamfer_distance)

result = housing