import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 12.0
height = 45.0
base_thickness = 5.0
groove_depth = 2.0
groove_width = 4.0
groove_position = 20.0
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
mount_hole_offset = 10.0

# Base profile for revolve (composite shape)
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height - base_thickness)
    .lineTo(inner_radius, height - base_thickness)
    .lineTo(inner_radius, base_thickness)
    .lineTo(0, base_thickness)
    .close()
)

# Revolve to create axisymmetric block
result = profile.revolve()

# Peripheral groove (cylindrical cut)
groove_cutter = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(outer_radius - groove_depth)
    .extrude(groove_width)
    .translate((0, 0, groove_position))
)
result = result.cut(groove_cutter)

# Chamfer on bottom face edges
result = result.faces("<Z").edges().chamfer(chamfer_size)

# Mounting holes on top face (patterned)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, mount_hole_offset), (mount_hole_spacing/2, mount_hole_offset)])
    .hole(mount_hole_diameter)
)
