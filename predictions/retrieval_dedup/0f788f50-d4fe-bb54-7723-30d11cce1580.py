import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
corner_fillet_radius = 3.0
edge_chamfer = 0.5
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
vent_hole_diameter = 3.0
vent_spacing = 10.0
vent_rows = 5
vent_cols = 6
recess_length = 30.0
recess_width = 20.0
circle_cut_diameter = 6.0
rib_height = 1.5
rib_extra = 4.0

# Base plate
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Rectangular recess cut through top face
result = (
    result
    .faces("+Z")
    .workplane()
    .rect(recess_length, recess_width)
    .cutBlind(plate_thickness)
)

# Circular cutout near one corner through top face
result = (
    result
    .faces("+Z")
    .workplane()
    .center(plate_length/2 - 12.0, plate_width/2 - 12.0)
    .circle(circle_cut_diameter/2)
    .cutBlind(plate_thickness)
)

# Apply corner fillets on all vertical outer edges
result = (
    result
    .edges("|Z")
    .fillet(corner_fillet_radius)
)

# Apply a small chamfer on top perimeter edges for safety
result = (
    result
    .edges(">Z")
    .chamfer(edge_chamfer)
)

# Mounting holes near each corner
mount_positions = [
    (mount_hole_offset, mount_hole_offset),
    (-mount_hole_offset, mount_hole_offset),
    (mount_hole_offset, -mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
]
for x, y in mount_positions:
    result = (
        result
        .faces("+Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(mount_hole_diameter)
    )

# Vent hole grid on top face
result = (
    result
    .faces("+Z")
    .workplane()
    .rarray(vent_spacing, vent_spacing, vent_cols, vent_rows, center=True)
    .hole(vent_hole_diameter)
)

# Reinforcing rib on back side under the recess area
rib_length = recess_length + rib_extra
rib_width = recess_width + rib_extra
result = (
    result
    .faces("-Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)

# Final solid stored in result