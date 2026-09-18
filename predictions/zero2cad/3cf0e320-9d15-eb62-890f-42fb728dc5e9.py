import cadquery as cq
import math

# Parameters
num_teeth = 42
module = 1.5
pitch_diameter = module * num_teeth
pitch_radius = pitch_diameter / 2.0
addendum = module
dedendum = 1.25 * module
outer_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum
gear_thickness = 15.0
helix_angle_deg = 20.0
helix_angle_rad = math.radians(helix_angle_deg)
# Twist angle for helical extrusion
twist_angle = (gear_thickness * math.tan(helix_angle_rad) * 360.0) / (math.pi * pitch_diameter)
central_hole_diameter = 8.0
mount_hole_diameter = 3.0
mount_hole_radius = 0.7 * pitch_radius
mount_hole_count = 3
mount_hole_angle = 360.0 / mount_hole_count

# Generate gear outline points alternating outer and root radii
points = []
for i in range(num_teeth * 2):
    angle = i * math.pi / num_teeth
    radius = outer_radius if i % 2 == 0 else root_radius
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    points.append((x, y))

# Build gear solid with helical twist
gear = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .twistExtrude(gear_thickness, twist_angle)
)

# Central bore
gear = gear.faces(">Z").workplane().hole(central_hole_diameter)

# Mounting holes pattern on top face
gear = (
    gear.faces(">Z")
    .workplane()
    .polarArray(mount_hole_radius, 0, mount_hole_angle, mount_hole_count)
    .hole(mount_hole_diameter)
)

result = gear