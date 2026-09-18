import cadquery as cq

arm_length = 80.0
arm_width = 30.0
arm_height = 20.0
shell_thickness = 2.0
rib_thickness = 3.0
rib_spacing = 10.0
rib_end_margin = 5.0
hole_diameter = 10.0
hole_depth = 12.0
chamfer_distance = 1.0

# Outer solid
outer = (cq.Workplane("XY")
    .sketch()
    .rect(arm_width, arm_height)
    .finalize()
    .extrude(arm_length)
)

# Hollow shell
shell = outer.shell(-shell_thickness)

# Determine rib count and positions
inner_width = arm_width - 2 * shell_thickness
x_count = int(inner_width // rib_spacing)
if x_count < 2:
    x_count = 2
x_spacing = inner_width / (x_count - 1) if x_count > 1 else inner_width
start_x = -inner_width / 2

# Create rib solid (single rib centered at origin)
rib_profile = (cq.Workplane("XY")
    .sketch()
    .rect(rib_thickness, arm_height - 2 * shell_thickness)
    .finalize()
    .extrude(arm_length - 2 * rib_end_margin)
    .translate((0, 0, rib_end_margin))
)

# Assemble ribs inside the shell
ribs = cq.Workplane("XY")
for i in range(x_count):
    x_pos = start_x + i * x_spacing
    ribs = ribs.union(rib_profile.translate((x_pos, 0, 0)))

# Combine shell and ribs
body = shell.union(ribs)

# Blind sensor mount hole (centered on X, Y on end face)
body = (body.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter, depth=hole_depth)
)

# Chamfer outer vertical edges
body = body.edges("|Z").chamfer(chamfer_distance)

result = body