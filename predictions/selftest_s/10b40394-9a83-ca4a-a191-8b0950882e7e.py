import cadquery as cq

# Parameters
sleeve_outer_dia = 60.0
sleeve_inner_dia = 40.0
sleeve_length = 30.0
base_thickness = 10.0
base_width = 80.0
fillet_radius = 2.0
chamfer_dist = 1.0
mount_hole_dia = 5.0
mount_hole_offset = 20.0
rib_height = 6.0
rib_width = 8.0
rib_count = 6

# Base profile for revolve
profile = (
    cq.Workplane("XZ")
    .lineTo(sleeve_outer_dia / 2, 0)
    .lineTo(sleeve_outer_dia / 2, sleeve_length)
    .lineTo(base_width / 2, sleeve_length)
    .lineTo(base_width / 2, sleeve_length + base_thickness)
    .lineTo(0, sleeve_length + base_thickness)
    .close()
)

# Revolve to create sleeve with base flange
sleeve = profile.revolve()

# Remove inner material to create hollow support
inner_cylinder = (
    cq.Workplane("XY")
    .circle(sleeve_inner_dia / 2)
    .extrude(sleeve_length + base_thickness)
)
sleeve = sleeve.cut(inner_cylinder)

# Add mounting holes on top face of base flange
for x, y in [
    (mount_hole_offset, mount_hole_offset),
    (-mount_hole_offset, mount_hole_offset),
    (mount_hole_offset, -mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
]:
    sleeve = (
        sleeve
        .faces(">Z")
        .workplane()
        .center(x, y)
        .hole(mount_hole_dia)
    )

# Create a single rib profile to reinforce the outer wall
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, sleeve_length)
    .translate((sleeve_outer_dia / 2 + rib_width / 2, 0, sleeve_length / 2))
)

# Replicate ribs around the circumference
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rib_instance = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    sleeve = sleeve.union(rib_instance)

# Apply a chamfer on the outer top edge of the base flange
sleeve = sleeve.edges("|Z and >Y").chamfer(chamfer_dist)

# Apply a fillet on the outer cylindrical surface to smooth the diameter transition
result = sleeve.edges("|Z").fillet(fillet_radius)
