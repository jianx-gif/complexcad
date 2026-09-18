import cadquery as cq
import math

# Primary dimensions (max 100 units)
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
step_radius = 60.0
inner_radius = 40.0
block_height = 30.0
step_height = 12.0
top_height = block_height - step_height
arc_angle_deg = 120.0
thread_diameter = 10.0
thread_length = 15.0
clearance_extra = 1.0
through_hole_diameter = thread_diameter + clearance_extra
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_radius = 30.0
mount_hole_count = 6
mount_hole_spacing_angle = 360.0 / mount_hole_count

# Profile for revolve (XZ plane)
profile = (
    cq.Workplane('XZ')
    .lineTo(outer_radius, 0)
    .vLine(block_height)
    .lineTo(step_radius, block_height)
    .vLine(-step_height)
    .lineTo(inner_radius, top_height)
    .vLine(-top_height)
    .close()
)

# Revolve to create the stepped arc block
arc_block = (
    profile
    .revolve(angleDegrees=arc_angle_deg)
    .edges('|Z')
    .chamfer(chamfer_distance)
)

# Central clearance hole (through)
arc_block = (
    arc_block
    .faces('>Z')
    .workplane()
    .hole(through_hole_diameter)
)

# Threaded insert pocket (blind hole) centered on axis
arc_block = (
    arc_block
    .faces('>Z')
    .workplane()
    .hole(thread_diameter, depth=thread_length)
)

# Mounting holes patterned around outer cylindrical surface
result = (
    arc_block
    .faces('>X')
    .workplane(centerOption='CenterOfMass')
    .polarArray(radius=mount_hole_radius, startAngle=0, angle=mount_hole_spacing_angle, count=mount_hole_count)
    .hole(mount_hole_diameter)
)
