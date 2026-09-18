import cadquery as cq

# Parameters
body_length = 80.0
inlet_radius = 20.0
outlet_radius = 12.0
outlet_taper_length = 20.0
wall_thickness = 4.0
flange_thickness = 6.0
flange_radius = 30.0
fillet_radius = 2.0
rib_thickness = 2.0
rib_height = wall_thickness - 1.0
rib_spacing = 10.0
rib_start_offset = flange_thickness + wall_thickness

# Derived dimensions
inner_radius = inlet_radius - wall_thickness
outer_body_length = body_length - outlet_taper_length
rib_count = int((outer_body_length - rib_start_offset) / rib_spacing)

# Main body (XZ plane) revolving profile
main_body = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (inlet_radius, 0),
        (inlet_radius, outer_body_length),
        (outlet_radius, body_length),
        (0, body_length),
    ])
    .close()
    .revolve()
)

# Inlet flange with filleted bottom edge
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
    .faces("<Z")
    .fillet(fillet_radius)
)

# Assemble main body and flange
assembly = main_body.union(flange)

# Rib profile (XZ) revolved
rib_profile = (
    cq.Workplane("XZ")
    .polyline([
        (inner_radius, 0),
        (inner_radius, rib_height),
        (inner_radius + rib_thickness, rib_height),
        (inner_radius + rib_thickness, 0),
    ])
    .close()
    .revolve()
)

# Distribute ribs along the length
ribs = cq.Workplane("XY")
for i in range(rib_count):
    z_pos = rib_start_offset + i * rib_spacing
    ribs = ribs.union(rib_profile.translate((0, 0, z_pos)))

# Integrate ribs
assembly = assembly.union(ribs)

result = assembly