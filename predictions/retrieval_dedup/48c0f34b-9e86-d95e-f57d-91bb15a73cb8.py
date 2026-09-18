
import cadquery as cq

# Primary dimensions (max 100 units)
outer_diameter = 70.0
flange_diameter = 85.0
flange_thickness = 8.0
block_length = 60.0
taper_length = 20.0
inner_diameter = 20.0
bearing_seat_diameter = 30.0
bearing_seat_depth = 30.0
mount_hole_diameter = 5.0
mount_hole_spacing = 40.0
key_slot_length = 30.0
key_slot_width = 4.0
key_slot_depth = 8.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
flange_radius = flange_diameter / 2.0
inner_radius = inner_diameter / 2.0
seat_radius = bearing_seat_diameter / 2.0
total_length = block_length + taper_length
body_length = block_length - taper_length

# Outer profile on XZ plane, revolve about Y axis
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, flange_radius)
    .lineTo(flange_thickness, flange_radius)
    .lineTo(flange_thickness + body_length, outer_radius)
    .lineTo(total_length, outer_radius - (outer_radius - seat_radius) * (taper_length / taper_length))
    .lineTo(total_length, 0)
    .close()
)

solid = profile.revolve()

# Central bore
central_cyl = (
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(inner_radius)
    .extrude(total_length + 2)
)
solid = solid.cut(central_cyl)

# Bearing seat cavity
seat_start = flange_thickness + body_length - bearing_seat_depth
seat_cyl = (
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(seat_radius)
    .extrude(bearing_seat_depth)
    .translate(cq.Vector(0, seat_start, 0))
)
solid = solid.cut(seat_cyl)

# Mounting holes (two)
for x_off in (-mount_hole_spacing / 2.0, mount_hole_spacing / 2.0):
    hole_cyl = (
        cq.Workplane("XZ")
        .center(x_off, 0)
        .circle(mount_hole_diameter / 2.0)
        .extrude(total_length + 2)
    )
    solid = solid.cut(hole_cyl)

# Key slot on side surface
slot_center_y = total_length / 2.0
slot = (
    cq.Workplane("XZ")
    .center(outer_radius - key_slot_width / 2.0, 0)
    .rect(key_slot_width, key_slot_length)
    .extrude(key_slot_depth)
    .translate(cq.Vector(0, slot_center_y, 0))
)
solid = solid.cut(slot)

result = solid
