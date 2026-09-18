import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 8.0
base_height = 10.0
taper_height = 30.0
top_height = 15.0
taper_top_radius = 20.0
rib_thickness = 2.0
rib_height = 12.0
rib_count = 6
chamfer_size = 1.0
slot_width = 4.0
slot_length = 20.0
slot_depth = 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_height)
    .lineTo(taper_top_radius, base_height + taper_height)
    .lineTo(outer_radius, base_height + taper_height)
    .lineTo(outer_radius, base_height + taper_height + top_height)
    .lineTo(inner_radius, base_height + taper_height + top_height)
    .close()
)

# Revolve to create the main body
body = profile.revolve()

# Add internal ribs
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(taper_height)
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

body = body.union(ribs)

# Add a side slot for cable access
slot = (
    cq.Workplane("XY")
    .center(outer_radius - slot_depth / 2, 0)
    .rect(slot_width, slot_length)
    .extrude(slot_depth)
    .translate((0, 0, base_height + taper_height / 2))
)

body = body.cut(slot)

# Apply chamfer to top outer edge
body = body.faces(">Z").edges().chamfer(chamfer_size)

result = body