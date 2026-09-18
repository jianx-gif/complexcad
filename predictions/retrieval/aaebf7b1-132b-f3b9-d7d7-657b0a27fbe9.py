import cadquery as cq

# Parameters
outer_radius = 45.0
wall_thickness = 3.0
dome_height = 40.0
rib_height = 8.0
rib_width = 10.0
rim_chamfer = 1.0

# Outer profile (XZ plane) for revolve around Y axis
profile = (
    cq.Workplane("XZ")
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius - rib_width, rib_height)
    .threePointArc((outer_radius - rib_width/2, rib_height + rib_width/2), (0, dome_height))
    .close()
)

solid = profile.revolve()

# Chamfer rim before shell
chamfered = solid.faces("<Z").edges().chamfer(rim_chamfer)

# Shell to create thin wall
result = chamfered.shell(wall_thickness)
