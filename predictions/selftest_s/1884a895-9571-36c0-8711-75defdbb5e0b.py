import cadquery as cq

# Parameters
plate_leg1 = 70.0
plate_leg2 = 40.0
plate_width = 30.0
sheet_thickness = 4.0
bend_radius = 5.0
hole_diameter = 6.0
hole_spacing_x = 20.0
hole_spacing_y = 20.0
holes_per_leg1 = 3
holes_per_leg2 = 2
hole_edge_clearance = 8.0
chamfer_distance = 1.0

# Cross‑section profile (width x thickness)
profile = (
    cq.Workplane("YZ")
    .rect(sheet_thickness, plate_width)
    .wire()
)

# Center‑line path with 90° bend
path = (
    cq.Workplane("XY")
    .lineTo(plate_leg1, 0)
    .threePointArc((plate_leg1 + bend_radius, bend_radius), (plate_leg1 + bend_radius, 2 * bend_radius))
    .lineTo(plate_leg1 + bend_radius, 2 * bend_radius + plate_leg2)
    .wire()
)

# Sweep to create bent block
block = profile.sweep(path, makeSolid=True)

# Generate hole positions on horizontal leg
hole_points = []
for i in range(holes_per_leg1):
    x = hole_edge_clearance + i * hole_spacing_x
    y = plate_width / 2.0
    hole_points.append((x, y))
# Generate hole positions on vertical leg
for j in range(holes_per_leg2):
    x = plate_leg1 + bend_radius
    y = plate_width / 2.0 + hole_edge_clearance + j * hole_spacing_y
    hole_points.append((x, y))

# Create hole solid
holes = (
    cq.Workplane("XY")
    .pushPoints(hole_points)
    .circle(hole_diameter / 2.0)
    .extrude(sheet_thickness)
)

# Subtract holes
part = block.cut(holes)

# Apply chamfer to outer edges
result = part.edges().chamfer(chamfer_distance)
