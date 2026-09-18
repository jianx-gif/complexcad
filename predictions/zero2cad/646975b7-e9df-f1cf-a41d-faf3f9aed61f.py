import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius_base = 25.0
inner_radius_top = 20.0
height = 40.0
base_thickness = 5.0
fillet_radius = 1.0
slot_width = 2.0
slot_length = 30.0
slot_depth = 2.0
slot_center_z = height / 2.0

# Outer solid via revolve of a rectangular profile
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(0, height)
    .close()
)
outer_solid = outer_profile.revolve()

# Inner tapered cavity via revolve of a triangular profile
inner_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(inner_radius_base, 0)
    .lineTo(inner_radius_top, height)
    .lineTo(0, height)
    .close()
)
inner_cavity = inner_profile.revolve()

# Subtract inner cavity to create socket
socket_body = outer_solid.cut(inner_cavity)

# Fillet all edges for safety
socket_body = socket_body.edges().fillet(fillet_radius)

# Create a rectangular slot solid for cutting
slot_solid = (
    cq.Workplane("XY")
    .box(slot_depth, slot_length, slot_width, centered=(True, True, True))
    .translate((outer_radius - slot_depth / 2.0, 0, slot_center_z))
)

# Cut the slot from the socket
result = socket_body.cut(slot_solid)
