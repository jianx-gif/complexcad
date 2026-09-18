import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 15.0
arm_height = 10.0
wall_thickness = 0.8
boss_diameter = 12.0
boss_height = 10.0
hole_diameter = 3.0
hole_spacing = 10.0
num_holes = 5
chamfer_dist = 0.5
round_cap_radius = 1.0

# Central boss
boss = cq.Workplane('XY').circle(boss_diameter/2).extrude(boss_height)

# Sweep profile for arm
profile = cq.Workplane('XY').rect(arm_width, arm_height).wire()
path_pts = [
    (0, 0, 0),
    (arm_length*0.3, 0, arm_width*0.2),
    (arm_length, 0, 0)
]
path = cq.Workplane('XY').spline(path_pts).wire()
arm_solid = profile.sweep(path, multisection=False)

# Create thin wall by shelling
arm_shell = arm_solid.shell(-wall_thickness)

# Combine boss and arm
combined = boss.union(arm_shell)

# Patterned holes along the arm (drilled perpendicular to XY plane)
for i in range(num_holes):
    x_pos = (i+1) * hole_spacing
    if x_pos >= arm_length:
        break
    hole = cq.Workplane('XY').center(x_pos - arm_length/2, 0).circle(hole_diameter/2).extrude(arm_width*2)
    combined = combined.cut(hole)

# Chamfer distal edge (edges at maximum X)
combined = combined.edges('>>X').chamfer(chamfer_dist)

# Rounded distal cap using a small sphere fused at tip
cap = cq.Workplane('XY').center(arm_length, 0).sphere(round_cap_radius)
combined = combined.union(cap)

result = combined