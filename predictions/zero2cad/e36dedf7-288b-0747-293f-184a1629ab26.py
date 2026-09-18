import cadquery as cq

# Parameters
cap_outer_diameter = 80.0
cap_height = 30.0
wall_thickness = 5.0
flange_diameter = 100.0
flange_thickness = 4.0
groove_width = 12.0
groove_depth = 4.0
groove_offset_from_top = 6.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_count = 4

# Derived dimensions
cap_outer_radius = cap_outer_diameter / 2.0
cap_inner_radius = cap_outer_radius - wall_thickness
flange_radius = flange_diameter / 2.0

# Base cap profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(flange_radius, 0)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(cap_outer_radius, flange_thickness)
    .lineTo(cap_outer_radius, cap_height - groove_offset_from_top)
    .lineTo(cap_inner_radius, cap_height - groove_offset_from_top)
    .lineTo(cap_inner_radius, cap_height)
    .lineTo(0, cap_height)
    .close()
)

cap = profile.revolve()

# Recessed groove on top surface
cap = (
    cap.faces(">Z")
    .workplane()
    .rect(groove_width, groove_depth)
    .cutBlind(-groove_depth)
)

# Chamfer outer top edge
cap = cap.faces(">Z").edges().chamfer(chamfer_size)

# Mounting holes on flange (bottom face)
cap = (
    cap.faces("<Z")
    .workplane()
    .rarray(mount_hole_spacing, 0, mount_hole_count, 1)
    .hole(mount_hole_diameter)
)

result = cap