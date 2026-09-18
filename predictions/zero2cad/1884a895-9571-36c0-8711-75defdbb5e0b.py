import cadquery as cq

# Parameters
leg_length = 60.0
leg_width = 40.0
wall_thickness = 3.0
corner_radius = 6.0
extrude_depth = 20.0
hole_diameter = 4.0
hole_spacing = 15.0
hole_offset = 10.0
chamfer_size = 0.7

# Outer L profile points (clockwise)
outer_profile = [
    (0, 0),
    (leg_length, 0),
    (leg_length, leg_width),
    (leg_length - wall_thickness, leg_width),
    (leg_length - wall_thickness, wall_thickness),
    (0, wall_thickness),
]

# Create solid by extruding outer profile
result = (
    cq.Workplane("XY")
    .polyline(outer_profile)
    .close()
    .extrude(extrude_depth)
)

# Apply interior fillet to create rounded inner corner
result = result.edges("|Z").filter(
    lambda e: abs(e.Center().x - (leg_length - wall_thickness)) < 0.01
    and abs(e.Center().y - wall_thickness) < 0.01
).fillet(corner_radius)

# Drill clearance holes on the +X face (horizontal leg)
result = (
    result.faces(">X")
    .workplane()
    .center(hole_offset, extrude_depth / 2)
    .rarray(hole_spacing, 0, 3, 1)
    .circle(hole_diameter / 2)
    .cutBlind(-wall_thickness)
)

# Drill clearance holes on the +Y face (vertical leg)
result = (
    result.faces(">Y")
    .workplane()
    .center(hole_offset, extrude_depth / 2)
    .rarray(hole_spacing, 0, 3, 1)
    .circle(hole_diameter / 2)
    .cutBlind(-wall_thickness)
)

# Apply chamfer to all outer edges for safety
result = result.edges().chamfer(chamfer_size)
