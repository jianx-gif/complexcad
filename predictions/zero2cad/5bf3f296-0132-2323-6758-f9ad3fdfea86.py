import cadquery as cq

# Parameters
base_diameter = 40.0
top_width = 60.0
top_height = 30.0
loft_height = 40.0
central_bore_diameter = 20.0
mount_hole_diameter = 8.0
mount_hole_spacing = 45.0
fillet_radius = 3.0
rib_thickness = 4.0
rib_height = 10.0
rib_spacing = 12.0
pocket_width = 30.0
pocket_depth = 5.0
set_screw_diameter = 4.0
set_screw_offset = 12.0

# Base loft between circle and rectangle
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .workplane(offset=loft_height)
    .rect(top_width, top_height)
    .loft()
)

# Fillet top perimeter edges for safety
result = result.faces(">Z").edges().fillet(fillet_radius)

# Central bore through entire part
result = result.faces(">Z").workplane().hole(central_bore_diameter)

# Mounting holes on top face, symmetric about center
mount_points = [(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)]
result = result.faces(">Z").workplane().pushPoints(mount_points).hole(mount_hole_diameter)

# Set screw clearance hole on top face, offset from center
result = (
    result.faces(">Z")
    .workplane()
    .center(set_screw_offset, 0)
    .hole(set_screw_diameter)
)

# Recessed pocket on top face for weight reduction
result = (
    result.faces(">Z")
    .workplane()
    .rect(pocket_width, pocket_width)
    .cutBlind(-pocket_depth)
)

# Add ribs on the +Y side face for stiffness
rib_count = int((loft_height - rib_spacing) // rib_spacing)
for i in range(rib_count):
    z_pos = rib_spacing * (i + 1)
    result = (
        result.faces(">Y")
        .workplane()
        .center(0, z_pos)
        .rect(rib_thickness, rib_height)
        .cutBlind(-rib_thickness)
    )

# Add ribs on the -Y side face for stiffness
for i in range(rib_count):
    z_pos = rib_spacing * (i + 1)
    result = (
        result.faces("<Y")
        .workplane()
        .center(0, z_pos)
        .rect(rib_thickness, rib_height)
        .cutBlind(-rib_thickness)
    )
