import cadquery as cq

# Parameters
outer_radius = 40.0
inner_radius = 20.0
step_radius = 15.0
block_height = 60.0
step_height = 20.0
groove_width = 5.0
groove_depth = 3.0
groove_center_z = 30.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_offset = 10.0
hole_spacing = 30.0

# Base profile for revolve (XY plane, revolve about Z)
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, block_height - step_height)
    .lineTo(inner_radius, block_height - step_height)
    .lineTo(inner_radius, block_height)
    .lineTo(step_radius, block_height)
    .lineTo(step_radius, groove_center_z + groove_width / 2)
    .lineTo(step_radius - groove_depth, groove_center_z + groove_width / 2)
    .lineTo(step_radius - groove_depth, groove_center_z - groove_width / 2)
    .lineTo(step_radius, groove_center_z - groove_width / 2)
    .lineTo(step_radius, 0)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Chamfer outer edges
solid = solid.edges().chamfer(chamfer_size)

# Add mounting holes on top face
hole_positions = [(-hole_spacing / 2, 0), (hole_spacing / 2, 0)]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Add a rectangular pocket on the side for weight reduction
pocket_width = 12.0
pocket_height = 20.0
pocket_depth = 4.0
solid = (
    solid.faces("<Z")
    .workplane(offset=block_height / 2)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

result = solid