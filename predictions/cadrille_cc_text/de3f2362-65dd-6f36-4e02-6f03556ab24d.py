import cadquery as cq
base_socket_radius = 12.0
housing_height = 80.0
top_cover_height = 40.0
top_cover_width = 60.0
top_cover_depth = 20.0
vent_slot_width = 30.0
vent_slot_height = 5.0
vent_slot_depth = 20.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(housing_height, housing_height)
    .extrude(housing_height)
)
top_cut = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(top_cover_depth)
    .extrude(top_cover_height)
)
housing = base.cut(top_cut)
housing = housing.edges().chamfer(chamfer_distance)
housing = (
    housing.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(vent_slot_width, vent_slot_height)
    .cutBlind(-vent_slot_depth)
)
housing = (
    housing.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
result = housing
