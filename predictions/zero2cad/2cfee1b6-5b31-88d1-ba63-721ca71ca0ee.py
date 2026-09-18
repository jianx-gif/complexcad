import cadquery as cq

# Parameters
outer_diameter = 60.0
wall_thickness = 2.0
cap_height = 30.0
top_fillet_radius = 3.0
chamfer_distance = 0.5
vent_slot_width = 4.0
vent_slot_height = 12.0
vent_slot_depth = wall_thickness + 0.2
vent_slot_count = 8
vent_slot_angle_offset = 0.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create outer profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, cap_height - top_fillet_radius)
    .threePointArc((top_fillet_radius, cap_height), (outer_radius, cap_height))
    .lineTo(outer_radius, 0)
    .close()
)

# Revolve profile to create solid cap
solid_cap = profile.revolve()

# Shell to create thin wall
hollow_cap = solid_cap.shell(-wall_thickness)

# Apply chamfer to all edges for safety
chamfered_cap = hollow_cap.edges().chamfer(chamfer_distance)

# Create vent slots on outer cylindrical surface
vent_slots = (
    cq.Workplane("XY")
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=vent_slot_angle_offset, angle=360, count=vent_slot_count)
    .rect(vent_slot_width, vent_slot_height)
    .extrude(vent_slot_depth)
)

# Cut vent slots from the cap
result = chamfered_cap.cut(vent_slots)
