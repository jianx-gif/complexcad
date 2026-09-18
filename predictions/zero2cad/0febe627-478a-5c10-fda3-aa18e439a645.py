import cadquery as cq

# Parameters
cover_length = 80.0
cover_width = 60.0
cover_height = 12.0
wall_thickness = 2.0
lip_height = 1.5
lip_extension = 2.0
vent_hole_diameter = 3.0
vent_rows = 3
vent_cols = 4
vent_spacing_x = 10.0
vent_spacing_y = 12.0
chamfer_distance = 1.0

# Base solid
base = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_height)
)

# Thin-walled shell
shell = base.shell(-wall_thickness)

# Chamfer outer edges of the shell
shell_chamfered = shell.edges().chamfer(chamfer_distance)

# Ventilation holes on top face
vented = (
    shell_chamfered.faces(">Z")
    .workplane()
    .rarray(vent_spacing_x, vent_spacing_y, vent_cols, vent_rows)
    .circle(vent_hole_diameter / 2)
    .cutThruAll()
)

# Snap‑fit lip around perimeter on top face
lip = (
    vented.faces(">Z")
    .workplane()
    .rect(cover_length + 2 * lip_extension, cover_width + 2 * lip_extension)
    .extrude(lip_height)
)

# Combine shell with lip
result = vented.union(lip)
