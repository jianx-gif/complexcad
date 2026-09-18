import cadquery as cq

# Parameters
outer_diameter = 60.0
inner_diameter = 20.0
collar_length = 20.0
shoulder_length = 5.0
fillet_radius = 2.0
chamfer_distance = 1.0
set_screw_diameter = 4.0
set_screw_depth = 8.0
set_screw_offset = 12.0
slot_width = 6.0
slot_length = 10.0
slot_depth = 4.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
shoulder_start = collar_length - shoulder_length

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, shoulder_start)
    .threePointArc((outer_radius, shoulder_start + fillet_radius), (outer_radius, shoulder_start))
    .lineTo(outer_radius, collar_length)
    .lineTo(inner_radius, collar_length)
    .close()
)

# Revolve to create collar
result = profile.revolve()

# Chamfer outer top and bottom edges
result = result.faces(">Z").edges().chamfer(chamfer_distance)
result = result.faces("<Z").edges().chamfer(chamfer_distance)

# Set screw holes (radial cylinders)
set_screw_cyl = (
    cq.Workplane("YZ")
    .circle(set_screw_diameter / 2.0)
    .extrude(set_screw_depth)
    .translate((outer_radius - set_screw_depth / 2.0, 0, set_screw_offset))
)
set_screw_cyl2 = set_screw_cyl.rotate((0, 0, 0), (0, 0, 1), 180)
result = result.cut(set_screw_cyl).cut(set_screw_cyl2)

# Slot on outer surface (rectangular pocket)
slot = (
    cq.Workplane("YZ")
    .rect(slot_length, slot_width)
    .extrude(slot_depth)
    .translate((outer_radius - slot_depth / 2.0, 0, collar_length / 2.0))
)
result = result.cut(slot)
