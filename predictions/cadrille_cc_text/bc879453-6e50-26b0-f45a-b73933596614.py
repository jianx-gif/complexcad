import cadquery as cq
outer_dia = 70.0
wall_thickness = 5.0
cap_height = 20.0
lip_height = 20.0
lip_chamfer = 0.8
blind_hole_dia = 30.0
blind_hole_depth = 12.0
vent_slot_width = 6.0
vent_slot_depth = 3.0
vent_slot_count = 4
outer_radius = outer_dia / 2.0
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(cap_height)
)
lip = (
    cq.Workplane("XY")
    .circle(lip_height)
    .extrude(lip_height)
    .translate((0, 0, cap_height - lip_height))
)
cap = base.cut(lip)
cap = (
    cap.faces(">Z")
    .workplane()
    .circle(blind_hole_dia / 2.0)
    .cutBlind(blind_hole_depth)
)
cap = cap.faces(">Z").edges().chamfer(lip_chamfer)
result = (
    cap
    .faces(">Z")
    .workplane()
    .circle(blind_hole_dia / 2.0)
    .cutBlind(blind_hole_depth)
)
