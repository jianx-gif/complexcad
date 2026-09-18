import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
corner_fillet_radius = 5.0
mount_hole_diameter = 6.0
mount_hole_spacing = 40.0
mount_hole_count = 4
mount_hole_diameter = 8.0
mount_hole_spacing = 20.0
rib_height = 4.0
rib_thickness = 5.0
rib_spacing = 20.0
rib_count = 4
chamfer_distance = 0.8
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
base = base.edges("|Z").fillet(corner_fillet_radius)
base = base.edges("|Z").chamfer(chamfer_distance)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(plate_length - 2 * mount_hole_spacing, plate_width - 2 * mount_hole_spacing)
    .extrude(plate_thickness)
)
base = base.edges("|Z").chamfer(chamfer_distance)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_distance)
result = base
