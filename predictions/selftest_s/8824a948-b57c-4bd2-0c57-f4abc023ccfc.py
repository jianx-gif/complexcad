import cadquery as cq
BS = cq.selectors.BoxSelector
base_radius = 20
shoulder_radius = 30
base_height = 10
shoulder_height = 8
vent_width = 4
vent_depth = 2
chamfer_distance = 0.5
mount_hole_diam = 5
mount_hole_offset = 5
central_bore_diam = 10
profile = (
    cq.Workplane("XY")
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(shoulder_radius, base_height)
    .lineTo(shoulder_radius, base_height + shoulder_height)
    .lineTo(0, base_height + shoulder_height)
    .close()
)
shoulder_body = profile.revolve()
vent = (
    cq.Workplane("XY")
    .box(vent_width, vent_depth, base_height + shoulder_height, centered=(True, True, False))
    .translate((shoulder_radius - vent_width/2, 0, 0))
)
result = (
    shoulder_body
    .cut(vent)
    .workplane(offset=0)
    .pushPoints([
        (base_radius - mount_hole_offset, 0),
        (-base_radius + mount_hole_offset, 0),
        (0, base_radius - mount_hole_offset),
        (0, -base_radius + mount_hole_offset)
    ])
    .hole(mount_hole_diam)
    .faces(">Z")
    .hole(central_bore_diam)
    .faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
)
