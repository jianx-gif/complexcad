import cadquery as cq

# Parameters
inner_radius = 30
outer_radius = 40
height = 20
rib_height = 5
rib_radial_extra = 3
screw_hole_diameter = 4
screw_hole_depth = 8
shell_thickness = 2

# Base annular tube profile
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
)

# Revolve to create solid tube
solid = profile.revolve(360)

# Create thin-walled shell
thin_wall = solid.shell(shell_thickness)

# Peripheral rib as an outward cylinder on top region
rib = (
    cq.Workplane("XY")
    .cylinder(rib_height, outer_radius + rib_radial_extra)
    .translate((0, 0, height - rib_height))
)

# Combine rib with shell
combined = thin_wall.union(rib)

# Set-screw blind hole through rib
result = (
    combined
    .faces(">Z")
    .workplane()
    .hole(screw_hole_diameter, depth=screw_hole_depth)
)
