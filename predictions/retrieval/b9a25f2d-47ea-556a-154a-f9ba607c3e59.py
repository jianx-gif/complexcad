import cadquery as cq
import math

# Primary dimensions
linear_width = 60.0
block_depth = 15.0
block_height = 12.0
arc_outer_diameter = 100.0
vertical_fillet = 1.0
top_fillet = 1.5
edge_chamfer = 0.5

# Derived dimensions
arc_outer_radius = 0.5 * arc_outer_diameter
arc_center_diameter = arc_outer_diameter - block_depth
arc_center_radius = 0.5 * arc_center_diameter
arc_center_angle = math.degrees(math.acos((2 * arc_center_radius**2 - linear_width**2) / (2 * arc_center_radius**2)))
arc_secant_angle = 0.5 * (180.0 - arc_center_angle)

# Central boss dimensions
boss_radius = 0.25 * arc_center_radius
boss_height = 6.0

# Countersunk hole dimensions
bolt_diameter = 4.5
head_diameter = 8.0
head_height = 3.0
hole_spacing = 8.0
hole_count = 3

# Path for sweep (arc)
path = (
    cq.Workplane("XY")
    .radiusArc((linear_width, 0.0), arc_center_radius)
    .wire()
)

# Main arc block body created by sweeping a rectangle along the arc
block_body = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -arc_secant_angle, 0))
    .rect(block_depth, block_height)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(vertical_fillet)
    .edges(">Z")
    .fillet(top_fillet)
)

# Add central cylindrical boss on top of block
with_boss = (
    block_body
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)

# Pattern of countersunk holes along boss diameter
result = (
    with_boss
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rarray(hole_spacing, 0, hole_count, 1)
    .cboreHole(bolt_diameter, head_diameter, head_height)
)
