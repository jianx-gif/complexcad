import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 30.0
bracket_thickness = 5.0
rib_height = 12.0
rib_width = 20.0
rib_thickness = 4.0
hole_diameter = 5.0
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 4
chamfer_distance = 1.0
fillet_radius = 0.8

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Rib on top face, centered
rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)

# Combine base and rib
combined = base.union(rib)

# Generate hole positions (grid centered)
points = []
start_x = -((hole_cols - 1) * hole_spacing_x) / 2
start_y = -((hole_rows - 1) * hole_spacing_y) / 2
for i in range(hole_cols):
    for j in range(hole_rows):
        points.append((start_x + i * hole_spacing_x, start_y + j * hole_spacing_y))

# Drill holes through the part
with_holes = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)

# Apply chamfer to all outer edges
chamfered = with_holes.edges().chamfer(chamfer_distance)

# Apply small fillet to top edges for safety
result = chamfered.edges(">Z").fillet(fillet_radius)
