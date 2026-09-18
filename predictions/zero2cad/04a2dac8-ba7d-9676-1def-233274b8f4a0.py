import cadquery as cq

# Parameters
outer_radius = 20.0
inner_radius = 15.0
sleeve_length = 60.0
flange_thickness = 5.0
flange_radius = 25.0
slot_width = 6.0
slot_length = 20.0
slot_offset = 15.0
chamfer_size = 0.8

# Base sleeve profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .threePointArc((outer_radius + 2, sleeve_length / 2), (outer_radius, sleeve_length))
    .lineTo(inner_radius, sleeve_length)
    .close()
)

sleeve = profile.revolve()

# Flange at the bottom (Z=0)
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Combine sleeve and flange
combined = sleeve.union(flange)

# Slot cut through the sleeve wall (centered on X axis)
slot = (
    cq.Workplane("XY")
    .center(0, slot_offset)
    .rect(slot_length, slot_width)
    .extrude(sleeve_length + flange_thickness)
)

# Apply slot cut
result = combined.cut(slot)

# Chamfer outer cylindrical edge for safety
result = result.edges("|Z").chamfer(chamfer_size)
