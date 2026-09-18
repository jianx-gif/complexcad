import cadquery as cq

# Parameters
housing_length = 80.0
outer_radius = 30.0
wall_thickness = 3.0
shaft_radius = 8.0
shaft_recess_depth = 12.0
rib_width = 6.0
rib_thickness = 2.0
rib_count = 6
chamfer_size = 0.8

# Base outer cylinder
base_cylinder = cq.Workplane("XY").cylinder(height=housing_length, radius=outer_radius)

# Shell to create thin-walled cylinder
hollow_cylinder = base_cylinder.faces(">Z").shell(wall_thickness)

# Internal ribs creation
rib = (
    cq.Workplane("YZ")
    .rect(rib_width, housing_length)
    .extrude(rib_thickness)
    .translate((outer_radius - wall_thickness - rib_thickness/2, 0, 0))
)

rib_pattern = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    rib_pattern = rib_pattern.union(rib.rotate((0,0,0), (0,0,1), angle))

# Combine ribs with hollow cylinder
cylinder_with_ribs = hollow_cylinder.union(rib_pattern)

# Recessed shaft opening at top end
shaft_cut = (
    cq.Workplane("XY")
    .center(0, 0)
    .cylinder(height=shaft_recess_depth, radius=shaft_radius)
    .translate((0, 0, housing_length/2 - shaft_recess_depth/2))
)

# Subtract shaft opening
cylinder_with_hole = cylinder_with_ribs.cut(shaft_cut)

# Add chamfer on outer edge
result = cylinder_with_hole.edges("|Z").chamfer(chamfer_size)
