import cadquery as cq
import math

# Parameters
bellows_length = 70.0
inner_radius = 22.0
wall_thickness = 8.0
corrugation_amplitude = 4.0
corrugation_period = 6.0
num_corrugations = int(bellows_length / corrugation_period)
outer_radius = inner_radius + wall_thickness

groove_axial_length = 6.0
groove_depth = 3.0
chamfer_size = 0.3

boss_radius = wall_thickness / 4.0

mount_hole_diameter = 4.0
mount_hole_count = 4
mount_hole_offset_radius = outer_radius - wall_thickness / 2.0

# Build bellows profile points on XZ plane
points = [(0, 0), (inner_radius + wall_thickness, 0)]
z = 0.0
for i in range(num_corrugations * 2):
    z += corrugation_period / 2.0
    r = inner_radius + wall_thickness
    if i % 2 == 0:
        r += corrugation_amplitude
    points.append((r, z))
points.append((0, z))

# Create revolved bellows solid
bellows = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)

# Add an internal cylindrical boss for reinforcement
boss = (
    cq.Workplane("XY")
    .center(inner_radius + wall_thickness / 2, 0)
    .circle(boss_radius)
    .extrude(bellows_length)
)
bellows = bellows.union(boss)

# Chamfer edges for safety before further modifications
bellows = bellows.edges().chamfer(chamfer_size)

# Recessed clamp groove at inlet (bottom face) – rectangular pocket into outer wall
bellows = (
    bellows.faces("<Z")
    .workplane(invert=True)
    .rect(outer_radius * 2, groove_axial_length)
    .cutBlind(-groove_depth)
)

# Create mounting holes through outer wall at mid-height
hole_centers = []
for i in range(mount_hole_count):
    angle = (2 * math.pi / mount_hole_count) * i
    hole_centers.append((mount_hole_offset_radius * math.cos(angle),
                         mount_hole_offset_radius * math.sin(angle)))
holes = (
    cq.Workplane("XY")
    .workplane(offset=bellows_length / 2)
    .pushPoints(hole_centers)
    .circle(mount_hole_diameter / 2)
    .extrude(wall_thickness * 2)
)
bellows = bellows.cut(holes)

result = bellows