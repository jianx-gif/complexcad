import cadquery as cq
total_height = 70.0
base_radius = 30.0
shoulder_fillet = 2.0
shoulder_radius = base_radius + shoulder_fillet
shoulder_radius = shoulder_radius + shoulder_radius
shoulder_fillet = shoulder_fillet + shoulder_radius
pin_bottom_radius = 12.0
pin_top_radius = 5.0
pin_length = 30.0
blind_hole_dia = 6.0
blind_hole_depth = 20.0
mount_hole_dia = 4.0
mount_hole_radius = 25.0
chamfer_dist = 2.0
rib_radius = 3.0
rib_height = base_radius + shoulder_fillet
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, total_height - shoulder_radius)
    .threePointArc((base_radius + shoulder_radius, total_height), (shoulder_radius, total_height))
    .lineTo(shoulder_radius, total_height)
    .lineTo(shoulder_radius, total_height - shoulder_radius)
    .lineTo(shoulder_radius, total_height - shoulder_radius)
    .lineTo(0, total_height - shoulder_radius)
    .close()
)
result = profile.revolve()
result = result.edges().chamfer(chamfer_dist)
result = (
    result.faces(">Z")
    .workplane()
    .hole(blind_hole_dia, depth=blind_hole_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=pin_plate_radius, count=pin_length, startAngle=0, angle=360)
    .hole(mount_hole_dia)
)
