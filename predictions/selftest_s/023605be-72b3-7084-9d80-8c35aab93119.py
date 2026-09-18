import cadquery as cq
import math
length = 80.0
width = 50.0
thickness = 10.0
dovetail_length = 60.0
dovetail_width = 12.0
dovetail_depth = 6.0
dovetail_angle = 20.0
counterbore_diameter = 12.0
counterbore_depth = 5.0
set_screw_hole_dia = 8.0
mount_hole_dia = 5.0
mount_hole_offset = 8.0
rib_width = 8.0
rib_height = 5.0
rib_count = 3
rib_margin = 10.0
fillet_radius = 0.5
chamfer_distance = 1.0
side_offset = dovetail_depth * math.tan(math.radians(dovetail_angle))
part = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
)
part = (
    part.faces(">Y")
    .workplane()
    .polyline([
        (-dovetail_length/2, 0),
        (dovetail_length/2, 0),
        (dovetail_length/2 - side_offset, -dovetail_depth),
        (-dovetail_length/2 + side_offset, -dovetail_depth)
    ])
    .close()
    .cutBlind(-dovetail_depth)
)
part = (
    part.faces(">X")
    .workplane()
    .center(length/2 - 10.0, 0)
    .cboreHole(set_screw_hole_dia, counterbore_diameter, counterbore_depth)
)
mount_points = [
    (-length/2 + mount_hole_offset, -thickness/2 + mount_hole_offset),
    ( length/2 - mount_hole_offset, -thickness/2 + mount_hole_offset),
    (-length/2 + mount_hole_offset,  thickness/2 - mount_hole_offset),
    ( length/2 - mount_hole_offset,  thickness/2 - mount_hole_offset)
]
part = (
    part.faces("-Y")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_dia)
)
rib_spacing = (length - 2 * rib_margin) / (rib_count - 1)
rib_points = [(-length/2 + rib_margin + i * rib_spacing, 0) for i in range(rib_count)]
part = (
    part.faces(">Z")
    .workplane()
    .pushPoints(rib_points)
    .rect(rib_width, rib_height)
    .cutBlind(rib_height)
)
result = part.edges("|Z").chamfer(chamfer_distance)
result = result.faces(">Z").edges().fillet(fillet_radius)
