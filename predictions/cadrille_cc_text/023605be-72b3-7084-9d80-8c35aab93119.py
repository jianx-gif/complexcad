import cadquery as cq
length = 80.0
width = 50.0
thickness = 10.0
dovetail_length = 60.0
dovetail_width = 12.0
dovetail_depth = 6.0
dovetail_angle = 20.0
counterbore_diameter = 12.0
counterbore_depth = 5.0
mount_hole_dia = 8.0
mount_hole_offset = 8.0
fillet_radius = 0.5
chamfer_distance = 1.0
rib_width = 8.0
rib_height = 5.0
rib_length = width - 2 * thickness
rib_count = int((length - 2 * thickness) // rib_length) + 1
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (dovetail_length, 0),
        (dovetail_length, thickness),
        (dovetail_width, thickness),
        (dovetail_width, thickness + thickness),
        (0, thickness + thickness + thickness + 0.5),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_length)
    .cutBlind(-rib_height)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(counterbore_diameter, counterbore_diameter, counterbore_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(counterbore_diameter, counterbore_diameter, counterbore_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_length)
    .cutBlind(-rib_height)
)
result = base
