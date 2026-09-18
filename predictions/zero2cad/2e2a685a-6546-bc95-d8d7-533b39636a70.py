import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 6.0
step_length = 50.0
step_width = 30.0
step_height = 4.0
fillet_radius = 1.0
hole_diameter = 5.0
hole_depth = 4.0
mount_hole_diameter = 4.0
mount_hole_spacing = 25.0
rib_width = 6.0
rib_height = 10.0
rib_spacing = 20.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Stepped shoulder on top of base
step = (
    cq.Workplane("XY")
    .workplane(offset=bracket_thickness)
    .rect(step_length, step_width)
    .extrude(step_height)
)

# Combine base and step
bracket = base.union(step)

# Fillet vertical edges of the stepped shoulder (edges parallel to Z)
bracket = bracket.edges("|Z").fillet(fillet_radius)

# Blind tapped hole in the step (centered on step)
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .center(step_length/2, step_width/2)
    .hole(hole_diameter, depth=hole_depth)
)

# Mounting holes on the base plate (two holes symmetric about center)
bracket = (
    bracket
    .faces("<Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

# Add ribs on the top surface of the base plate for stiffness
rib_count = int((bracket_length - rib_spacing) // rib_spacing)
for i in range(rib_count):
    x_pos = -bracket_length/2 + rib_spacing/2 + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .workplane(offset=bracket_thickness)
        .center(x_pos, 0)
        .rect(rib_width, bracket_width)
        .extrude(rib_height)
    )
    bracket = bracket.union(rib)

result = bracket