import cadquery as cq

# Primary dimensions
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
inner_diameter_step1 = 30.0
inner_radius_step1 = inner_diameter_step1 / 2.0
inner_diameter_step2 = 40.0
inner_radius_step2 = inner_diameter_step2 / 2.0
block_height = 60.0
oil_inlet_diameter = 10.0
mount_hole_diameter = 8.0
mount_hole_offset = 20.0
chamfer_size = 2.0
relief_width = 15.0
relief_depth = 8.0
relief_dist_from_bottom = 20.0
rib_extra = 5.0
rib_lower_ratio = 0.2
rib_upper_ratio = 0.4

# Base revolve profile on XZ plane (half-section)
profile = (
    cq.Workplane('XZ')
    .lineTo(outer_radius, 0)
    .threePointArc((outer_radius, block_height * 0.05), (outer_radius * 0.95, block_height * 0.1))
    .lineTo(outer_radius, block_height)
    .lineTo(inner_radius_step2, block_height)
    .lineTo(inner_radius_step2, block_height * 0.6)
    .lineTo(inner_radius_step1, block_height * 0.6)
    .lineTo(inner_radius_step1, 0)
    .close()
)

# Revolve to create bearing block
solid = profile.revolve()

# Chamfer lower outer edge
solid = solid.faces("<Z").edges().chamfer(chamfer_size)

# Central oil inlet through top face
solid = solid.faces(">Z").workplane().hole(oil_inlet_diameter)

# Symmetric mounting holes on top face
mount_points = [(mount_hole_offset, 0), (-mount_hole_offset, 0)]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

# Side relief pocket cut into outer cylindrical wall
solid = (
    solid.faces(">X")
    .workplane(offset=-2)  # offset inward from outer face
    .rect(relief_width, relief_depth)
    .cutBlind(-relief_depth)
)

# Internal reinforcing rib (thin wall) revolving a rectangular slab
rib = (
    cq.Workplane('XZ')
    .center(inner_radius_step1, block_height * rib_lower_ratio)
    .lineTo(inner_radius_step1 + rib_extra, block_height * rib_lower_ratio)
    .lineTo(inner_radius_step1 + rib_extra, block_height * rib_upper_ratio)
    .lineTo(inner_radius_step1, block_height * rib_upper_ratio)
    .close()
    .revolve()
)
solid = solid.union(rib)

result = solid
