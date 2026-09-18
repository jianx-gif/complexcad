import cadquery as cq

# Parameters
outer_radius = 30.0
flange_radius = 45.0
body_length = 60.0
flange_thickness = 10.0
wall_thickness = 2.0
chamfer_size = 1.0
mount_hole_diameter = 6.0
mount_hole_spacing = 40.0
rib_width = 8.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 15.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, body_length)
    .lineTo(flange_radius, body_length)
    .lineTo(flange_radius, body_length + flange_thickness)
    .lineTo(0, body_length + flange_thickness)
    .close()
)

# Revolve to create solid body
solid_body = profile.revolve()

# Shell to create thin-walled housing
hollow_body = solid_body.shell(wall_thickness)

# Chamfer outer edge of flange (top face perimeter)
chamfered_body = hollow_body.faces(">Z").edges().chamfer(chamfer_size)

# Add mounting holes on top flange (two opposite holes)
with_holes = (
    chamfered_body
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

# Add internal ribs for stiffness (radial ribs inside the cavity)
# Create a single rib profile and array it around the axis
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

# Position ribs at several axial locations inside the cavity
rib_positions = [body_length/2 - rib_spacing, body_length/2, body_length/2 + rib_spacing]
rib_assembly = cq.Workplane("XY")
for z in rib_positions:
    rib_assembly = rib_assembly.union(
        rib.translate((0, 0, z))
    )

# Combine ribs with the main body
result = with_holes.union(rib_assembly)
