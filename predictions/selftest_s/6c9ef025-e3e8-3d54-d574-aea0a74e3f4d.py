import cadquery as cq
import math

# Parameters
pipe_od = 30.0
pipe_wall = 4.0
pipe_id = pipe_od - 2 * pipe_wall
elbow_center_radius = 40.0
elbow_angle_deg = 60.0
fillet_radius = 1.0
flange_extra_radius = 5.0
flange_length = 10.0
hole_diameter = 4.0

# Derived radii for profile
outer_radius = elbow_center_radius + pipe_od / 2.0
inner_radius = elbow_center_radius - pipe_od / 2.0

# Angles in radians
ang = math.radians(elbow_angle_deg)
mid_ang = ang / 2.0

# Points for outer arc
p0_outer = (outer_radius, 0)
p1_outer = (outer_radius * math.cos(ang), outer_radius * math.sin(ang))
mid_outer = (outer_radius * math.cos(mid_ang), outer_radius * math.sin(mid_ang))
# Points for inner arc
p0_inner = (inner_radius, 0)
p1_inner = (inner_radius * math.cos(ang), inner_radius * math.sin(ang))
mid_inner = (inner_radius * math.cos(mid_ang), inner_radius * math.sin(mid_ang))

# Sketch sector profile
profile = (
    cq.Workplane("XY")
    .moveTo(*p0_outer)
    .threePointArc(mid_outer, p1_outer)
    .lineTo(*p1_inner)
    .threePointArc(mid_inner, p0_inner)
    .close()
)

# Revolve sector to create elbow
elbow = profile.revolve(elbow_angle_deg)

# Fillet outer edge (edges farthest in +X direction)
outer_edges = elbow.edges(">X")
elbow = outer_edges.fillet(fillet_radius)

# Flange base cylinder (along Z)
base_cyl = (
    cq.Workplane()
    .center(0, 0)
    .circle(pipe_od / 2.0 + flange_extra_radius)
    .extrude(flange_length)
)

# Start flange (tangent +Y direction)
start_center = (elbow_center_radius, 0, 0)
start_flange = (
    base_cyl
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .translate(start_center)
)

# End flange (tangent direction at angle = elbow_angle_deg + 90)
end_center = (
    elbow_center_radius * math.cos(ang),
    elbow_center_radius * math.sin(ang),
    0,
)
end_tangent_angle = elbow_angle_deg + 90.0
end_flange = (
    base_cyl
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .rotate((0, 0, 0), (0, 0, 1), end_tangent_angle)
    .translate(end_center)
)

# Assemble elbow with flanges
assembly = elbow.union(start_flange).union(end_flange)

# Add mounting holes on start flange (four holes at 0,90,180,270 deg around flange center)
for i in range(4):
    angle_deg = i * 90.0
    theta = math.radians(angle_deg)
    hole_x = start_center[0] + (pipe_od / 2.0 + flange_extra_radius - 2.0) * math.cos(theta)
    hole_y = (pipe_od / 2.0 + flange_extra_radius - 2.0) * math.sin(theta)
    hole = (
        cq.Workplane("XY")
        .center(hole_x, hole_y)
        .circle(hole_diameter / 2.0)
        .extrude(flange_length + 2)
        .rotate((0, 0, 0), (1, 0, 0), 90)
    )
    assembly = assembly.cut(hole)

result = assembly