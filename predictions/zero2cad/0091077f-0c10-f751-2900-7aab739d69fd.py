import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 20.0
arm_thickness = 5.0
tip_length = 15.0
tip_fillet_radius = 1.0
base_fillet_radius = 1.5
hole_diameter = 4.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 2.0
rib_spacing = 12.0
rib_count = int((arm_length - tip_length) / rib_spacing)

# Base profile sketch on YZ plane
profile = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (arm_thickness, 0),
        (arm_thickness, arm_width / 2),
        (0, arm_width),
    ])
    .close()
)

# Extrude to create arm body
arm_body = profile.extrude(arm_length)

# Fillet at base edges (edges parallel to Z at the start of the arm)
arm_body = arm_body.edges("|Z and <X").fillet(base_fillet_radius)

# Fillet at tip edges (edges parallel to Z at the end of the arm)
arm_body = arm_body.edges("|Z and >X").fillet(tip_fillet_radius)

# Add mounting holes through the thickness near the base
hole_positions = [hole_offset, arm_length - hole_offset]
for x_pos in hole_positions:
    arm_body = (
        arm_body.faces("<Z")
        .workplane(centerOption="CenterOfMass")
        .center(x_pos - arm_length / 2, 0)
        .hole(hole_diameter)
    )

# Add ribs on the back side (negative Y) for stiffness
rib_start = tip_length + rib_spacing / 2
for i in range(rib_count):
    rib_x = rib_start + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .center(rib_x - arm_length / 2, -arm_thickness / 2 - rib_height / 2)
        .rect(rib_width, rib_height)
        .extrude(rib_height)
    )
    arm_body = arm_body.union(rib)

# Add a clearance slot near the tip for a pin
slot_width = 3.0
slot_length = 10.0
slot = (
    cq.Workplane("XY")
    .center(arm_length - tip_length / 2 - slot_length / 2, 0)
    .rect(slot_length, slot_width)
    .extrude(arm_thickness + 0.1)
)
arm_body = arm_body.cut(slot)

result = arm_body