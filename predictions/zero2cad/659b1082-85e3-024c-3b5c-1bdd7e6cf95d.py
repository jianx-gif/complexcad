import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 15.0
block_height = 45.0
shoulder_height = 10.0
fillet_radius = 2.0
hole_diameter = 10.0
hole_offset = 12.0
mount_hole_diameter = 5.0
mount_hole_spacing = 25.0
mount_hole_offset = 10.0
pocket_width = 12.0
pocket_depth = 4.0
pocket_offset = 5.0

# Base profile for revolve (YZ plane)
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, block_height - shoulder_height)
    .lineTo(inner_radius, block_height - shoulder_height)
    .threePointArc((inner_radius + fillet_radius, block_height - shoulder_height + fillet_radius), (inner_radius, block_height))
    .lineTo(outer_radius, block_height)
    .lineTo(outer_radius, 0)
    .close()
)

# Revolve to create axisymmetric block
result = profile.revolve()

# Through hole (offset from axis)
through_hole = (
    cq.Workplane("XZ")
    .center(hole_offset, block_height / 2)
    .circle(hole_diameter / 2)
    .extrude(2 * outer_radius)
)
result = result.cut(through_hole)

# Mounting holes on outer cylindrical face (two symmetric holes)
mount_hole = (
    cq.Workplane("YZ")
    .center(outer_radius, mount_hole_offset)
    .circle(mount_hole_diameter / 2)
    .extrude(2 * outer_radius)
)
result = result.cut(mount_hole)
mount_hole_mirror = (
    cq.Workplane("YZ")
    .center(-outer_radius, mount_hole_offset)
    .circle(mount_hole_diameter / 2)
    .extrude(2 * outer_radius)
)
result = result.cut(mount_hole_mirror)

# Rectangular pocket on outer surface for weight reduction
pocket = (
    cq.Workplane("YZ")
    .center(outer_radius - pocket_offset, block_height / 2)
    .rect(pocket_width, pocket_depth)
    .extrude(pocket_depth)
)
result = result.cut(pocket)
