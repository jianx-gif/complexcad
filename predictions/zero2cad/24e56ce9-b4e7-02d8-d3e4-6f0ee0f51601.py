import cadquery as cq

# Parameters
body_diameter = 60.0
body_length = 80.0
inlet_diameter = 40.0
inlet_length = 20.0
outlet_diameter = 30.0
outlet_length = 10.0
wall_thickness = 5.0
flange_diameter = 80.0
flange_thickness = 10.0
mount_hole_diameter = 6.0
mount_hole_count = 4
mount_hole_radius = 30.0
chamfer_size = 2.0
port_diameter = 15.0
port_offset = 20.0

# Derived dimensions
body_radius = body_diameter / 2.0
inlet_radius = inlet_diameter / 2.0
outlet_radius = outlet_diameter / 2.0
flange_radius = flange_diameter / 2.0
port_radius = port_diameter / 2.0

# Main body profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(body_radius, 0)
    .lineTo(body_radius, body_length - inlet_length - outlet_length)
    .lineTo(inlet_radius, body_length - outlet_length)
    .lineTo(inlet_radius, body_length)
    .lineTo(outlet_radius, body_length)
    .lineTo(outlet_radius, body_length + outlet_length)
    .lineTo(0, body_length + outlet_length)
    .close()
)
body = profile.revolve()

# Flange at base
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Combine body and flange
combined = body.union(flange)

# Mounting holes on flange (circular pattern)
mount_holes = (
    cq.Workplane("XY")
    .polarArray(mount_hole_radius, 0, 360, mount_hole_count)
    .circle(mount_hole_diameter / 2.0)
    .extrude(flange_thickness + 2.0)
)
combined = combined.cut(mount_holes)

# Internal flow channel (cylindrical bore) through body
channel = (
    cq.Workplane("XY")
    .circle(port_radius)
    .extrude(body_length + outlet_length + flange_thickness)
)
combined = combined.cut(channel)

# Side port hole (through side wall)
port = (
    cq.Workplane("XY")
    .center(port_offset, 0)
    .circle(port_radius)
    .extrude(body_length + outlet_length + flange_thickness)
)
combined = combined.cut(port)

# Chamfer on outlet edge (vertical edges)
combined = combined.edges("|Z").chamfer(chamfer_size)

result = combined