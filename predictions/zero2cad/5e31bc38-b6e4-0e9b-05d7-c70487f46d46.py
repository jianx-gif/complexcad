import cadquery as cq
import math

# Parameters
major_radius = 30.0
tube_radius = 10.0
wall_thickness = 2.0
fillet_radius = 3.0
hole_diameter = 4.0
hole_count = 6
boss_radius = 5.0
boss_height = 12.0

# Base torus solid
base_torus = (
    cq.Workplane("XY")
    .moveTo(major_radius, 0)
    .circle(tube_radius)
    .revolve(360)
)

# Thin-walled torus via shell
thin_torus = base_torus.shell(-wall_thickness)

# Central boss on inner side of torus
boss = (
    cq.Workplane("XY")
    .center(major_radius - tube_radius + wall_thickness/2, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)

# Combine torus and boss
combined = thin_torus.union(boss)

# Fillet outer edges (edges parallel to Z)
filleted = combined.edges("#Z").fillet(fillet_radius)

# Compute hole positions around torus
hole_positions = []
for i in range(hole_count):
    angle = 2 * math.pi * i / hole_count
    x = major_radius * math.cos(angle)
    y = major_radius * math.sin(angle)
    hole_positions.append((x, y))

# Drill holes through the torus wall
result = (
    filleted
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
