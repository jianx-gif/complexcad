import cadquery as cq

# Parameters
outer_radius = 40.0
inner_radius = 30.0
wall_thickness = outer_radius - inner_radius
height = 60.0
top_fillet_radius = 5.0
vent_slot_width = 4.0
vent_slot_height = 12.0
vent_slot_count = 12
vent_slot_depth = wall_thickness + 0.5
mount_hole_diameter = 6.0
mount_hole_offset = 15.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, height - top_fillet_radius)
    .threePointArc((outer_radius, height - top_fillet_radius), (outer_radius, height))
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
)

# Revolve to create housing
housing = profile.revolve(360, (0, 0, 1))

# Vent slots on outer cylindrical surface
vent_cuts = (
    cq.Workplane("XY")
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=0, angle=360, count=vent_slot_count)
    .rect(vent_slot_width, vent_slot_height)
    .extrude(vent_slot_depth)
)

housing = housing.cut(vent_cuts)

# Mounting hole through top face
housing = (
    housing.faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)

result = housing