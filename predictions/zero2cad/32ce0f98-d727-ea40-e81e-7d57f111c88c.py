import cadquery as cq
import math

# Parameters
pipe_outer_dia = 20.0
pipe_wall_thk = 2.0
pipe_inner_dia = pipe_outer_dia - 2 * pipe_wall_thk
elbow_center_radius = 30.0
elbow_angle_deg = 30.0
straight_length = 80.0
chamfer_dist = 0.5
hole_dia = 4.0
hole_spacing = 12.0
hole_rows = 2
hole_cols = 3
hole_depth = pipe_wall_thk - 0.5

# Derived dimensions
outer_radius = pipe_outer_dia / 2.0
inner_radius = pipe_inner_dia / 2.0
elbow_angle_rad = math.radians(elbow_angle_deg)

# Straight pipe segment (aligned with Z)
straight = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(straight_length)
)

# Elbow path (arc in XZ plane)
start_pt = (elbow_center_radius, 0, straight_length)
end_pt = (
    elbow_center_radius * math.cos(elbow_angle_rad),
    0,
    straight_length + elbow_center_radius * math.sin(elbow_angle_rad),
)
path = (
    cq.Workplane("XZ")
    .moveTo(*start_pt[:2])
    .radiusArc(end_pt[:2], elbow_center_radius)
    .wire()
)

# Sweep outer profile along path
outer_profile = cq.Workplane("XY").circle(outer_radius)
outer_elbow = outer_profile.sweep(path, multisection=False)

# Sweep inner profile (to create hollow)
inner_profile = cq.Workplane("XY").circle(inner_radius)
inner_elbow = inner_profile.sweep(path, multisection=False)

# Combine straight and elbow, then hollow
result = straight.union(outer_elbow).cut(inner_elbow)

# Chamfer outer edges for safety
result = result.edges().chamfer(chamfer_dist)

# Blind hole pattern on outer surface of straight section
result = (
    result.faces(">Z")
    .workplane()
    .rarray(hole_spacing, hole_spacing, hole_cols, hole_rows)
    .circle(hole_dia / 2.0)
    .cutBlind(hole_depth)
)
