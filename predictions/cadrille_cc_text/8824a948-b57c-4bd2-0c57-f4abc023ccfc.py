import cadquery as cq
base_radius = 20.0
base_height = 10.0
shoulder_radius = 30.0
shoulder_height = 8.0
vent_width = 4.0
vent_depth = 2.0
chamfer_distance = 0.5
central_bore_diam = 10.0
mount_hole_offset = 5.0
mount_hole_count = 4
base = (
    cq.Workplane("XY")
    .box(base_radius, base_height, base_height, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .hole(central_bore_diam)
)
shoulder = (
    cq.Workplane("XY")
    .center(0, base_height/2)
    .box(vent_width, vent_depth, vent_depth)
    .translate((0, 0, base_height/2 - vent_depth/2))
)
result = base.union(shoulder)
result = result.edges("|Z").chamfer(chamfer_distance)
result = result.edges("|Z").chamfer(chamfer_distance)
result = (
    result.faces(">Z")
    .workplane()
    .hole(central_bore_diam)
)
mount_hole = (
    cq.Workplane("XY")
    .center(0, 0)
    .hole(mount_hole_offset)
)
result = result.cut(mount_hole)
result = result.edges("|Z").chamfer(chamfer_distance)
