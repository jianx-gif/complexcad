import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 4.0
body_height = 20.0
lip_height = 3.0
lip_extension = 6.0
chamfer_distance = 2.0
set_screw_diameter = 4.0
set_screw_head_diameter = 7.0
set_screw_head_angle = 90.0
set_screw_offset = 12.0
rib_thickness = 2.0
rib_height = 10.0
rib_count = 4

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, body_height)
    .lineTo(outer_radius + lip_extension, body_height + lip_height)
    .lineTo(inner_radius, body_height + lip_height)
    .close()
)

# Revolve to create axisymmetric body
body = profile.revolve()

# Add internal ribs for stiffness (radial ribs)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness/2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(body_height)
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

body = body.union(ribs)

# Add set screw hole with countersink on top face
body = (
    body.faces(">Z")
    .workplane()
    .center(set_screw_offset, 0)
    .cskHole(set_screw_head_diameter, body_height + lip_height, set_screw_head_angle)
)

# Apply chamfer to top outer edge
result = body.faces(">Z").edges().chamfer(chamfer_distance)
