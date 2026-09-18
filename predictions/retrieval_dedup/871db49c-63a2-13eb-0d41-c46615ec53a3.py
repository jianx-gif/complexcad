import cadquery as cq

# Core dimensions
square_side = 10.0
oval_major = 25.0
oval_minor = 15.0
loft_height = 40.0
step_count = 5
boss_diameter = 8.0
boss_height = 12.0
counterbore_diameter = 12.0
counterbore_depth = 4.0
csk_depth = 1.5
csk_angle = 82.0

# Increment calculations for loft transition
step_height = loft_height / (step_count + 1)
major_inc = (oval_major - square_side) / (step_count + 1)
minor_inc = (oval_minor - square_side) / (step_count + 1)

# Base square profile
result = cq.Workplane("XY").rect(square_side, square_side)

# Intermediate loft profiles
for i in range(1, step_count + 1):
    z = step_height * i
    maj = square_side + major_inc * i
    minr = square_side + minor_inc * i
    if abs(maj - minr) < 1e-6:
        result = result.workplane(offset=z).rect(maj, minr)
    else:
        result = result.workplane(offset=z).ellipse(maj, minr)

# Top oval profile
result = result.workplane(offset=loft_height).ellipse(oval_major, oval_minor)

# Lofted body
result = result.loft(combine=True)

# Central boss
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Countersink for safety on boss top
result = (
    result
    .faces(">Z")
    .workplane()
    .cskHole(boss_diameter, csk_depth, csk_angle)
)

# Counterbore for screw engagement
result = (
    result
    .faces(">Z")
    .workplane()
    .cboreHole(boss_diameter, counterbore_diameter, boss_height, counterbore_depth)
)
