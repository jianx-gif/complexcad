import cadquery as cq

# Parameters
handle_length = 80.0
handle_radius = 12.0
grip_length = 40.0
flared_radius = 22.0
flare_length = 20.0
bolt_diameter = 6.0
knurl_height = 2.0
knurl_width = 1.5
knurl_depth = 0.4
knurl_pitch = 8.0
chamfer_size = 0.8

# Derived parameters
bolt_position = grip_length / 2.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(handle_radius, 0)
    .lineTo(handle_radius, grip_length)
    .lineTo(flared_radius, grip_length + flare_length)
    .lineTo(0, grip_length + flare_length)
    .lineTo(0, 0)
    .close()
)

# Revolve profile around Z axis to create handle body
solid = profile.revolve()

# Chamfer all edges for safety
solid = solid.edges().chamfer(chamfer_size)

# Through bolt hole centered on axis at bolt_position
solid = solid.workplane(offset=bolt_position).hole(bolt_diameter)

# Knurling on top face using polar array of rectangular cuts
num_knurls = int(360 / knurl_pitch)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=flared_radius - knurl_depth / 2, count=num_knurls, startAngle=0, angle=360)
    .rect(knurl_width, knurl_height)
    .cutBlind(knurl_depth)
)

result = solid
