import cadquery as cq
import math

# Parameters
elbow_angle_deg = 30
elbow_angle_rad = math.radians(elbow_angle_deg)
centerline_radius = 30.0
pipe_outer_dia = 20.0
pipe_wall_thickness = 2.0
pipe_inner_dia = pipe_outer_dia - 2 * pipe_wall_thickness
pipe_outer_radius = pipe_outer_dia / 2.0
pipe_inner_radius = pipe_inner_dia / 2.0
rib_width = 6.0
rib_height = 8.0
rib_thickness = 4.0
rib_angle_deg = 15.0
rib_angle_rad = math.radians(rib_angle_deg)
chamfer_dist = 0.5
hole_dia = 3.0
hole_spacing = 12.0

# Base elbow profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(centerline_radius + pipe_outer_radius, 0)
    .lineTo(centerline_radius + pipe_inner_radius, 0)
    .lineTo(centerline_radius + pipe_inner_radius, pipe_wall_thickness)
    .lineTo(centerline_radius + pipe_outer_radius, pipe_wall_thickness)
    .close()
)
elbow = profile.revolve(elbow_angle_deg)

# Reinforcement rib (YZ plane) positioned at specified angle
rib = (
    cq.Workplane("YZ")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((centerline_radius + pipe_outer_radius + rib_thickness / 2.0, 0, 0))
    .rotate((0, 0, 0), (0, 0, 1), rib_angle_deg)
)

# Combine elbow and rib
combined = elbow.union(rib)

# Add mounting holes on inlet face (normal +X)
combined = (
    combined.faces(">X")
    .workplane()
    .pushPoints([(-hole_spacing / 2.0, 0), (hole_spacing / 2.0, 0)])
    .hole(hole_dia)
)

# Apply chamfer to edges parallel to Z (outer edges)
result = combined.edges("|Z").chamfer(chamfer_dist)
