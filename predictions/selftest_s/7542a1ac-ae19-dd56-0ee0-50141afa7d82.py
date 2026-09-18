import cadquery as cq
import math
pipe_outer_dia = 30.0
pipe_wall_thk = 4.0
elbow_center_radius = 40.0
patch_width = 20.0
patch_thickness = 2.0
patch_angle_start_deg = 30.0
patch_angle_end_deg = 60.0
chamfer_len = 1.0
# Derived dimensions
inner_radius = pipe_outer_dia/2 - pipe_wall_thk
# Create elbow path (quarter circle)
path_elbow = (
    cq.Workplane("XZ")
    .moveTo(elbow_center_radius, 0)
    .threePointArc((0, elbow_center_radius/2), (0, elbow_center_radius))
    .wire()
    .val()
)
# Sweep outer pipe
outer_pipe = (
    cq.Workplane("XY")
    .circle(pipe_outer_dia/2)
    .sweep(path_elbow)
)
# Sweep inner cavity
inner_pipe = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .sweep(path_elbow)
)
pipe_elbow = outer_pipe.cut(inner_pipe)
# Reinforcement patch path on outer surface
patch_path_radius = elbow_center_radius + pipe_outer_dia/2
start_rad = math.radians(patch_angle_start_deg)
end_rad = math.radians(patch_angle_end_deg)
mid_rad = (start_rad + end_rad) / 2
start_pt = (patch_path_radius * math.cos(start_rad), patch_path_radius * math.sin(start_rad))
mid_pt = (patch_path_radius * math.cos(mid_rad), patch_path_radius * math.sin(mid_rad))
end_pt = (patch_path_radius * math.cos(end_rad), patch_path_radius * math.sin(end_rad))
path_patch = (
    cq.Workplane("XZ")
    .moveTo(start_pt[0], start_pt[1])
    .threePointArc(mid_pt, end_pt)
    .wire()
    .val()
)
# Sweep rectangular patch
patch = (
    cq.Workplane("XY")
    .rect(patch_width, patch_thickness)
    .sweep(path_patch)
)
# Position patch flush with outer surface by translating outward half thickness along radial direction (approximate using start normal)
# For simplicity, translate along Y axis (assuming Y is out of plane) to attach
patch = patch.translate((0, patch_thickness/2, 0))
# Combine
combined = pipe_elbow.union(patch)
# Add chamfer on inner edges of both ends
# Select edges at pipe openings: use faces with Z max/min? Actually ends are at X axis positive and Z axis positive
result = combined.edges("<<Z or >>Z").chamfer(chamfer_len)
