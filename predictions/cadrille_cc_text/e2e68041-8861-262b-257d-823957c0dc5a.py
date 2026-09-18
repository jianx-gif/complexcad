import cadquery as cq
handle_length = 80.0
handle_thickness = 20.0
handle_height = 12.0
flange_width = 35.0
flange_height = 6.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_spacing = 12.0
chamfer_distance = 1.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 12.0
rib_count = 4
rib_count = 5
slot_width = 4.0
slot_length = 25.0
slot_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(handle_length, handle_thickness)
    .extrude(handle_height)
)
flange = (
    cq.Workplane("XY")
    .rect(flange_width, handle_thickness)
    .extrude(flange_height)
    .translate((0, 0, handle_height))
)
flange = (
    cq.Workplane("XY")
    .rect(flange_width, handle_thickness)
    .extrude(flange_height)
    .translate((0, 0, handle_height))
)
flange = (
    flange.union(flange)
    .union(flange)
    .union(flange)
    .union(flange)
    .union(flange)
)
mount_hole = (
    cq.Workplane("XY")
    .center(0, 0)
    .cskHole(mount_hole_diameter, mount_hole_count, 360)
)
result = base.union(mount_hole)
result = result.edges("|Z").chamfer(chamfer_distance)
