import cadquery as cq

# Parameters
body_length = 80.0
body_radius = 25.0
wall_thickness = 2.0
inlet_radius = 12.0
inlet_length = 30.0
inlet_fillet_radius = 3.0
chamfer_distance = 0.5
mount_hole_diameter = 4.0
mount_hole_spacing = 40.0
mount_hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
central_bore_diameter = 6.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(body_radius, 0)
    .lineTo(body_radius, body_length - inlet_length)
    .threePointArc((body_radius + inlet_fillet_radius, body_length - inlet_length + inlet_fillet_radius),
                   (inlet_radius, body_length))
    .lineTo(0, body_length)
    .close()
)

# Revolve to create solid body
solid_body = profile.revolve()

# Shell to create thin-walled valve body
hollow_body = solid_body.shell(-wall_thickness)

# Chamfer outer edges for safety
hollow_body = hollow_body.edges().chamfer(chamfer_distance)

# Central bore through the valve body
hollow_body = hollow_body.faces(">Z").workplane().hole(central_bore_diameter)

# Mounting holes on side wall (two symmetric holes)
hole_cylinder = (
    cq.Workplane("YZ")
    .center(body_radius - wall_thickness/2, 0)
    .circle(mount_hole_diameter/2)
    .extrude(wall_thickness*2)
)

hole1 = hole_cylinder.translate((0, 0, mount_hole_offset))
hole2 = hole_cylinder.translate((0, 0, mount_hole_offset + mount_hole_spacing))

hollow_body = hollow_body.cut(hole1).cut(hole2)

# External reinforcement rib on outer surface
rib = (
    cq.Workplane("YZ")
    .center(body_radius, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

result = hollow_body.union(rib)
