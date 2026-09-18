import cadquery as cq

# Parameters
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
block_height = 70.0
step1_height = 20.0
step2_height = 30.0
step1_diameter = 60.0
step1_radius = step1_diameter / 2.0
bearing_diameter = 30.0
bearing_radius = bearing_diameter / 2.0
fillet_radius = 2.0
chamfer_distance = 1.5
mount_hole_diameter = 6.0
mount_hole_spacing = 40.0
mount_hole_offset = 15.0
# Radial groove parameters
groove_center_radius = bearing_radius + 5.0
groove_width = 6.0  # axial length of groove slot
groove_depth = 4.0  # radial depth into wall

# Base revolved profile
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, step1_height)
    .lineTo(step1_radius, step1_height)
    .lineTo(step1_radius, step1_height + step2_height)
    .lineTo(bearing_radius, step1_height + step2_height)
    .lineTo(bearing_radius, block_height)
    .lineTo(0, block_height)
    .close()
)

# Revolve to create solid
result = profile.revolve()

# Global fillet to smooth step transitions and other edges
result = result.fillet(fillet_radius)

# Central bearing bore through the entire height
bearing_bore = cq.Workplane("XY").center(0, 0).circle(bearing_radius).extrude(block_height)
result = result.cut(bearing_bore)

# Radial groove cut – rectangular pocket positioned at desired radius
groove_body = (
    cq.Workplane("XY")
    .center(groove_center_radius, step1_height + step2_height / 2)
    .rect(groove_depth, groove_width)
    .extrude(block_height)
)
result = result.cut(groove_body)

# Mounting holes on outer cylindrical face
mount_face = result.faces(">X").workplane()
mount_points = [(-mount_hole_spacing / 2, mount_hole_offset), (mount_hole_spacing / 2, mount_hole_offset)]
result = mount_face.pushPoints(mount_points).hole(mount_hole_diameter)
