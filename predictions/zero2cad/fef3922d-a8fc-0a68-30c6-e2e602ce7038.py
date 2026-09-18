import cadquery as cq

# Parameters
handle_length = 80.0
base_radius = 20.0
top_radius = 12.0
wall_thickness = 3.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 15.0
chamfer_distance = 2.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0

# Outer lofted body
outer_body = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=handle_length)
    .circle(top_radius)
    .loft()
)

# Hollow the body
hollow_body = outer_body.shell(-wall_thickness)

# Internal ribs
rib_count = int(handle_length / rib_spacing) + 1
ribs = (
    hollow_body.faces("<Z")
    .workplane()
    .rect(rib_width, rib_height)
    .rarray(rib_spacing, 0, rib_count, 1)
    .extrude(rib_thickness)
)

# Combine body and ribs
combined = hollow_body.union(ribs)

# Mounting hole through side wall
combined = (
    combined.faces(">X")
    .workplane()
    .center(0, mount_hole_offset)
    .hole(mount_hole_diameter)
)

# Chamfer outer edges
result = combined.edges("|Z").chamfer(chamfer_distance)
