import cadquery as cq

# Parameters
foot_length = 40.0
foot_width = 20.0
foot_thickness = 6.0
knob_diameter = 30.0
knob_height = 20.0
loft_steps = 5
step_height = knob_height / loft_steps
size_reduction_factor = 0.85
chamfer_distance = 1.0
hole_diameter = 4.0
hole_count = 4
hole_circle_radius = knob_diameter * 0.35
boss_diameter = knob_diameter * 0.4
rib_thickness = 2.0
rib_height = foot_thickness * 2
rib_length = foot_length * 0.5

# Base rectangular foot extruded
foot = cq.Workplane("XY").rect(foot_length, foot_width).extrude(foot_thickness)

# Build loft profiles
loft_builder = cq.Workplane("XY").workplane(offset=foot_thickness).rect(foot_length, foot_width)
current_length = foot_length
current_width = foot_width
for i in range(loft_steps):
    current_length *= size_reduction_factor
    current_width *= size_reduction_factor
    offset = foot_thickness + (i + 1) * step_height
    loft_builder = loft_builder.workplane(offset=offset).rect(current_length, current_width)
# Final circular knob profile
final_offset = foot_thickness + loft_steps * step_height
loft_builder = loft_builder.workplane(offset=final_offset).circle(knob_diameter / 2)

# Loft to create transition solid
transition = loft_builder.loft(combine=False)

# Combine foot and transition
result = foot.union(transition)

# Chamfer outer edges
result = result.edges().chamfer(chamfer_distance)

# Central boss on knob top
result = result.faces(">Z").workplane().circle(boss_diameter / 2).extrude(foot_thickness)

# Hole pattern on knob side (through the boss)
result = result.faces(">Z").workplane(offset=-foot_thickness/2).polarArray(0, 0, hole_circle_radius, hole_count).hole(hole_diameter)

# Add side rib for rigidity (attached to foot lower side)
result = result.faces("<Z").workplane().rect(rib_length, rib_thickness).extrude(rib_height)
