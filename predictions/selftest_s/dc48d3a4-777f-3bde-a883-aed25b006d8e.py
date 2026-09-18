import cadquery as cq

# Parameter definitions
total_height = 70
base_radius = 30
shoulder_fillet = 2
shoulder_radius = 20
pin_bottom_radius = 12
pin_top_radius = 5
pin_length = 30
blind_hole_dia = 6
blind_hole_depth = 20
chamfer_dist = 2
mount_hole_dia = 4
mount_hole_radius = 25
mount_hole_count = 4
rib_radius = 3
rib_height = total_height / 2

# Base revolved joint block profile using Workplane sketch
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, total_height - pin_length - shoulder_fillet)
    .threePointArc(
        (base_radius + shoulder_fillet, total_height - pin_length - shoulder_fillet / 2),
        (shoulder_radius, total_height - pin_length)
    )
    .lineTo(pin_bottom_radius, total_height)
    .lineTo(pin_top_radius, total_height)
    .lineTo(0, total_height)
    .close()
)

result = (
    profile
    .revolve()
    .edges("<Z").chamfer(chamfer_dist)
    .faces(">Z")
    .workplane()
    .hole(blind_hole_dia, blind_hole_depth)
    .faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_dia)
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .circle(rib_radius)
    .extrude(rib_height)
)
