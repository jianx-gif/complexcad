import cadquery as cq
import math
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
elbow_angle = 75.0
rib_height = 8.0
rib_width = 20.0
rib_start_angle = 20.0
rib_end_angle = rib_start_angle + rib_width
rib_start_rad = math.radians(rib_start_angle)
rib_end_rad = math.radians(rib_end_angle)
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 3
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_start_rad * outer_radius)
    .lineTo(outer_radius + rib_height, rib_start_rad * outer_radius)
    .lineTo(outer_radius + rib_height, rib_end_rad * outer_radius)
    .lineTo(outer_radius, rib_end_rad * outer_radius)
    .lineTo(outer_radius, elbow_angle * outer_radius)
    .lineTo(inner_radius, elbow_angle * outer_radius)
    .close()
)
elbow = profile.revolve(elbow_angle)
elbow = (
    elbow.faces(">X")
    .workplane()
    .rarray(0, hole_spacing, 1, hole_count)
    .hole(hole_diameter)
)
result = elbow