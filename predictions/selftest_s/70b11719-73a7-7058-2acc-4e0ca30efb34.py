import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
shoulder_height = 15.0
shoulder_width = 30.0
hole_diameter = 4.5
hole_spacing = 30.0
edge_chamfer = 1.0
relief_radius = 10.0
relief_depth = 6.0
rib_height = 3.0
rib_width = 5.0
rib_spacing = 15.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_length)
    .extrude(bracket_thickness)
)

# Shoulder (raised block) on one end of the plate (positive Y direction)
shoulder = (
    cq.Workplane("XY")
    .center(0, bracket_length/2 - shoulder_width/2)
    .rect(bracket_width, shoulder_width)
    .extrude(shoulder_height)
)

combined = base.union(shoulder)

# Relief pocket on the top of the shoulder (cylindrical pocket via circular cut)
relief_center_z = bracket_thickness + shoulder_height - relief_depth/2.0
combined = (
    combined.workplane(offset=relief_center_z)
    .center(0, bracket_length/2 - shoulder_width/2)
    .circle(relief_radius)
    .cutBlind(-relief_depth)
)

# Drill three evenly spaced M4 clearance holes through the part
hole_positions = [-hole_spacing, 0, hole_spacing]
for y in hole_positions:
    combined = (
        combined.workplane()
        .center(0, y)
        .hole(hole_diameter)
    )

# Add reinforcing ribs on the bottom side of the base plate
num_ribs = int((bracket_length - 2 * rib_spacing) // rib_spacing)
for i in range(num_ribs):
    rib_y = -bracket_length/2 + rib_spacing + i * rib_spacing
    combined = (
        combined.workplane(offset=0)
        .center(0, rib_y)
        .rect(rib_width, rib_spacing/2)
        .extrude(-rib_height)
    )

# Apply chamfer to all outer vertical edges for safety
combined = combined.edges("|Z").chamfer(edge_chamfer)

result = combined