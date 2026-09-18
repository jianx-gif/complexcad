import cadquery as cq

# Parametric dimensions (units: max 100 = 10 cm)
bracket_length = 80
bracket_width = 40
bracket_base_thickness = 6
flange_step_length = 50
flange_step_width = 30
flange_step_height = 4
corner_fillet_radius = 1
blind_hole_diameter = 5
blind_hole_depth = 8
blind_hole_x = bracket_length * 0.25
blind_hole_y = bracket_width / 2 - 10
mount_hole_diameter = 4
mount_hole_spacing = 25
mount_hole_offset = 10
rib_width = 6
rib_height = 10
rib_spacing = 20
chamfer_distance = 1

# Base bracket solid
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_base_thickness)
)

# Stepped flange on top of base
step = (
    cq.Workplane("XY")
    .workplane(offset=bracket_base_thickness)
    .rect(flange_step_length, flange_step_width)
    .extrude(flange_step_height)
)

bracket = base.union(step)

# Fillet interior vertical edges (provides the required filleted corner)
bracket = bracket.edges("|Z").fillet(corner_fillet_radius)

# Blind tapped hole into step (does not go through entire part)
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .center(blind_hole_x, blind_hole_y)
    .hole(blind_hole_diameter, blind_hole_depth)
)

# Mounting holes on bottom of base (two holes symmetric about center)
bracket = (
    bracket
    .faces("<Z")
    .workplane()
    .center(-mount_hole_spacing / 2, mount_hole_offset)
    .hole(mount_hole_diameter)
    .center(mount_hole_spacing, 0)
    .hole(mount_hole_diameter)
)

# Stiffening ribs along length, placed on top of base under the step
num_ribs = int((bracket_length - rib_spacing) // rib_spacing)
for i in range(num_ribs):
    x_pos = -bracket_length / 2 + rib_spacing / 2 + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .workplane(offset=bracket_base_thickness)
        .center(x_pos, 0)
        .rect(rib_width, bracket_width)
        .extrude(rib_height)
    )
    bracket = bracket.union(rib)

result = bracket