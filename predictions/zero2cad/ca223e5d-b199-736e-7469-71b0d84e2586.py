import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
channel_length = 70.0
notch_depth = 5.0
notch_start = 40.0
hole_diameter = 5.0
hole_count = 4
chamfer_size = 0.5
slot_width = 2.0
slot_height = 5.0
slot_depth = wall_thickness + 0.5

# Base profile with outward notch
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, notch_start)
    .lineTo(outer_radius + notch_depth, notch_start)
    .lineTo(outer_radius + notch_depth, channel_length)
    .lineTo(inner_radius, channel_length)
    .close()
)

# Revolve to create thin-walled channel
result = profile.revolve()

# Chamfer outer edges
result = result.edges("<Z or >Z").chamfer(chamfer_size)

# Add rectangular slots on outer surface at mid-height
mid_z = channel_length / 2.0
result = (
    result
    .workplane(offset=mid_z)
    .polarArray(radius=outer_radius + notch_depth/2, startAngle=0, angle=360, count=hole_count)
    .rect(slot_width, slot_height)
    .cutBlind(-slot_depth)
)

# Drill radial holes through wall at mid-height
result = (
    result
    .workplane(offset=mid_z)
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)
