import cadquery as cq

# Parameters
arm_length = 60.0
bracket_width = 30.0
thickness = 8.0
flange_length = 40.0
flange_extra_width = 20.0
rib_width = 6.0
rib_height = 6.0
rib_depth = 4.0
rib_spacing = 12.0
clearance_hole_dia = 5.0
mount_hole_dia = 4.0
mount_hole_offset = 10.0
chamfer_dist = 0.8

# Base arm
base = (
    cq.Workplane("XY")
    .rect(arm_length, bracket_width)
    .extrude(thickness)
)

# Flange positioned at the negative X side of the base
flange_center_x = -arm_length / 2 - flange_length / 2
flange = (
    cq.Workplane("XY")
    .rect(flange_length, bracket_width + flange_extra_width)
    .extrude(thickness)
    .translate((flange_center_x, 0, 0))
)

# Combine base and flange
combined = base.union(flange)

# Ribs on top of flange
rib_count = int((flange_length - 2 * rib_spacing) // rib_spacing) + 1
ribs = cq.Workplane("XY")
for i in range(rib_count):
    rib_x = flange_center_x - flange_length / 2 + rib_spacing + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_height)
        .extrude(rib_depth)
        .translate((rib_x, 0, thickness))
    )
    ribs = ribs.union(rib)
combined = combined.union(ribs)

# Clearance hole through the arm (cylinder cut)
clearance_hole = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(clearance_hole_dia / 2)
    .extrude(thickness)
)
combined = combined.cut(clearance_hole)

# Mounting holes on flange (two symmetric holes)
mount_hole_y = (bracket_width + flange_extra_width) / 2 - mount_hole_offset
mount_hole1 = (
    cq.Workplane("XY")
    .center(flange_center_x, mount_hole_y)
    .circle(mount_hole_dia / 2)
    .extrude(thickness)
)
mount_hole2 = (
    cq.Workplane("XY")
    .center(flange_center_x, -mount_hole_y)
    .circle(mount_hole_dia / 2)
    .extrude(thickness)
)
combined = combined.cut(mount_hole1).cut(mount_hole2)

# Chamfer all vertical edges
result = combined.edges("|Z").chamfer(chamfer_dist)
