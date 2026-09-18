
import cadquery as cq

plate_length = 100.0
plate_width = 80.0
plate_thickness = 6.0
pocket_length = 50.0
pocket_width = 40.0
pocket_depth = 4.0
hole_diameter = 5.0
countersink_diameter = 8.0
countersink_angle = 82.0
hole_spacing = 30.0
rib_thickness = 6.0
rib_length = 20.0
rib_height = 4.0
rib_offset = 5.0
chamfer_size = 0.5
fillet_radius = 1.0

# Base plate with chamfer on outer edges
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

result = result.edges("|X or |Y and >Z").chamfer(chamfer_size)

# Corner ribs for base support
def rib_at(x, y):
    return (
        cq.Workplane("XY")
        .center(x, y)
        .rect(rib_length, rib_thickness)
        .extrude(rib_height)
        .translate((0, 0, -rib_height))
    )

rib_coords = [
    (-(plate_length/2) + rib_offset + rib_length/2, -(plate_width/2) + rib_offset + rib_thickness/2),
    ((plate_length/2) - rib_offset - rib_length/2, -(plate_width/2) + rib_offset + rib_thickness/2),
    (-(plate_length/2) + rib_offset + rib_length/2, (plate_width/2) - rib_offset - rib_thickness/2),
    ((plate_length/2) - rib_offset - rib_length/2, (plate_width/2) - rib_offset - rib_thickness/2),
]

for xc, yc in rib_coords:
    result = result.union(rib_at(xc, yc))

# Central recessed pocket
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# Countersunk hole array 3x3
points = []
for i in range(-1, 2):
    for j in range(-1, 2):
        points.append((i * hole_spacing, j * hole_spacing))

result = (
    result.faces(">Z").workplane()
    .pushPoints(points)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, plate_thickness)
)

# Fillet vertical edges for safety
result = result.edges("|Z").fillet(fillet_radius)
