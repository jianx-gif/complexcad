import cadquery as cq
import math

# Parameters
plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
central_pocket_diameter = 24.0
central_pocket_depth = 5.0
countersink_hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 82.0
countersink_radius = 30.0
countersink_count = 6
chamfer_size = 0.8
rib_width = 6.0
rib_height = 2.0
rib_spacing = 15.0

# Base oval plate using ellipse extrusion
base_plate = (
    cq.Workplane("XY")
    .ellipse(plate_length / 2, plate_width / 2)
    .extrude(plate_thickness)
)

# Central recessed pocket (cylindrical cut)
central_pocket = (
    cq.Workplane("XY")
    .circle(central_pocket_diameter / 2)
    .extrude(central_pocket_depth)
    .translate((0, 0, plate_thickness - central_pocket_depth))
)

# Countersunk hole pattern on top surface
angle_step = 360.0 / countersink_count
points = [
    (
        countersink_radius * math.cos(math.radians(i * angle_step)),
        countersink_radius * math.sin(math.radians(i * angle_step))
    )
    for i in range(countersink_count)
]
countersink_holes = (
    base_plate.faces(">Z").workplane()
    .pushPoints(points)
    .cskHole(countersink_hole_diameter, countersink_diameter, countersink_angle)
)

# Reinforcing ribs on bottom surface (grid pattern)
rib_grid = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .vertices()
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)

# Assemble features
result = (
    base_plate
    .cut(central_pocket)
    .cut(countersink_holes)
    .union(rib_grid)
    .edges(">Z or <Z")
    .chamfer(chamfer_size)
)
