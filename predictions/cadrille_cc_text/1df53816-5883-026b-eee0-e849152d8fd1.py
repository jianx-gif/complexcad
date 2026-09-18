import cadquery as cq
base_width = 80.0
base_height = 70.0
thickness = 10.0
fillet_radius = 2.0
chamfer_distance = 1.5
slot_width = 15.0
slot_depth = 4.0
mount_hole_dia = 8.0
mount_hole_spacing = 60.0
rib_thickness = 3.0
rib_height = 15.0
rib_width = 20.0
rib_length = base_width - 2 * rib_width
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (base_width, 0),
        (base_width, thickness),
        (thickness, thickness),
        (thickness, base_height),
        (0, base_height),
    ])
    .close()
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(mount_hole_dia / 2)
    .cutBlind(-thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
base = base.union(rib)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_width, slot_depth)
    .extrude(thickness)
)
base = base.union(slot)
base = base.edges("|Z").chamfer(chamfer_distance)
result = base
