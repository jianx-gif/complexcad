import cadquery as cq
from math import sin, cos, radians

base_width = 60.0
base_depth = 30.0
base_thickness = 4.0
base_corner_radius = 2.0

arm_length = 50.0
arm_start_width = 20.0
arm_end_width = 8.0
arm_thickness = base_thickness
arm_angle = 45.0

pilot_hole_diameter = 3.0
pilot_hole_depth = 2.0
chamfer_distance = 1.0
fillet_radius = 0.8

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Trapezoidal arm profile
arm = (
    cq.Workplane("XY")
    .polyline([
        (-arm_start_width/2, 0),
        (arm_start_width/2, 0),
        (arm_end_width/2, arm_length),
        (-arm_end_width/2, arm_length),
    ])
    .close()
    .extrude(arm_thickness)
    .rotate((0, 0, 0), (0, 0, 1), arm_angle)
    .translate((0, base_depth/2, base_thickness))
)

# Combine base and arm
combined = base.union(arm)

# Pilot hole position in global coordinates
rad = radians(arm_angle)
pilot_offset = 0.8 * arm_length
pilot_x = pilot_offset * sin(rad)
pilot_y = base_depth/2 + pilot_offset * cos(rad)

# Cut recessed pilot hole
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(pilot_x, pilot_y)
    .circle(pilot_hole_diameter/2)
    .cutBlind(pilot_hole_depth)
)

# Chamfer outer vertical edges
combined = combined.edges("|Z").chamfer(chamfer_distance)

# Small fillet on remaining sharp edges
combined = combined.edges(">Z").fillet(fillet_radius)

result = combined
