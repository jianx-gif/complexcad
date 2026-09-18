import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 25.0
housing_height = 60.0
flange_height = 10.0
flange_radius = 45.0
wall_thickness = outer_radius - inner_radius
vent_slot_width = 5.0
vent_slot_height = 15.0
vent_slot_depth = wall_thickness + 0.5
vent_slot_count = 8
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset = 15.0
chamfer_size = 1.0

# Base profile for revolve (XY plane, revolve about X axis)
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, housing_height - flange_height)
    .threePointArc((outer_radius, housing_height - flange_height + 5), (outer_radius, housing_height - flange_height))
    .lineTo(flange_radius, housing_height - flange_height)
    .threePointArc((flange_radius - 5, housing_height), (flange_radius, housing_height))
    .lineTo(flange_radius, 0)
    .close()
)

# Revolve to create housing
housing = profile.revolve()

# Create vent slots as a compound of boxes positioned around circumference
vent_slots = cq.Workplane("XY")
for i in range(vent_slot_count):
    angle = i * 360.0 / vent_slot_count
    slot = (
        cq.Workplane("XY")
        .box(vent_slot_depth, vent_slot_width, vent_slot_height)
        .translate((outer_radius - vent_slot_depth / 2, 0, housing_height / 2))
        .rotate((0, 0, 0), (1, 0, 0), angle)
    )
    vent_slots = vent_slots.union(slot)

# Cut vent slots from housing
housing = housing.cut(vent_slots)

# Add mounting holes on the flange (two holes symmetric about Y axis)
mount_holes = (
    housing.faces(">X")
    .workplane()
    .pushPoints([(-mount_hole_spacing / 2, mount_hole_offset), (mount_hole_spacing / 2, mount_hole_offset)])
    .hole(mount_hole_diameter)
)

# Apply chamfer to outer edges
result = (
    mount_holes
    .edges("|X")
    .chamfer(chamfer_size)
)
