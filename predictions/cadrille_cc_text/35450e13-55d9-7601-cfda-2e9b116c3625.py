import cadquery as cq
plate_length = 80.0
plate_width = 50.0
plate_thickness = 10.0
blind_hole_diameter = 6.0
blind_hole_depth = 8.0
slot_length = 60.0
slot_width = 10.0
slot_depth = plate_thickness - 2.0
rib_width = 12.0
rib_height = 20.0
rib_thickness = 5.0
rib_offset = 8.0
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 12.0
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)
base = base.edges("|Z").chamfer(chamfer_size)
base = base.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_length, slot_width)
    .extrude(plate_thickness)
)
base = base.cut(slot)
base = base.edges("|Z").chamfer(chamfer_size)
base = base.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
result = base.union(rib)
