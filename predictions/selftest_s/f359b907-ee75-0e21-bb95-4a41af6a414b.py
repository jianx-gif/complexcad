import cadquery as cq
import math

# Parameters (max dimension 100)
gear_outer_radius = 45.0        # outer radius of gear
gear_thickness = 12.0           # gear thickness
bore_diameter = 30.0            # central bore diameter
chamfer_distance = 1.0          # small chamfer on outer edge
num_teeth = 24                  # number of teeth
tooth_depth = 6.0               # radial depth of each tooth

# Derived parameters
pitch_radius = gear_outer_radius - tooth_depth/2
half_tooth_angle = 360.0 / num_teeth * 0.5
tooth_width = 2 * pitch_radius * math.tan(math.radians(half_tooth_angle))

# Base gear body: revolved profile with central bore
base_body = (
    cq.Workplane("XZ")
    .moveTo(bore_diameter/2, -gear_thickness/2)
    .lineTo(gear_outer_radius, -gear_thickness/2)
    .lineTo(gear_outer_radius, gear_thickness/2)
    .lineTo(bore_diameter/2, gear_thickness/2)
    .close()
    .revolve(360, (0,0,0), (0,1,0))
)

# Add a functional mounting boss on the side
boss_radius = 5.0
boss_offset = gear_outer_radius/2
boss = (
    cq.Workplane("XY")
    .center(boss_offset, 0)
    .circle(boss_radius)
    .extrude(gear_thickness)
)
gear_with_boss = base_body.union(boss)

# Apply a small chamfer on all outer edges for safety
gear_chamfered = gear_with_boss.edges().chamfer(chamfer_distance)

# Create a single tooth solid positioned at the pitch radius
tooth_solid = (
    cq.Workplane("XY")
    .center(pitch_radius + tooth_depth/2, 0)
    .box(tooth_depth, tooth_width, gear_thickness)
)

# Build the full set of teeth by polar array (manual loop)
teeth = tooth_solid
for i in range(1, num_teeth):
    angle = i * 360.0 / num_teeth
    rotated = tooth_solid.rotate((0,0,0), (0,0,1), angle)
    teeth = teeth.union(rotated)

# Combine gear body with teeth (union) to form final gear
result = gear_chamfered.union(teeth)
