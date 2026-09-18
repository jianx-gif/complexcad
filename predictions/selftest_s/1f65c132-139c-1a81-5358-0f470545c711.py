import cadquery as cq

cover_length = 80.0
cover_width = 60.0
cover_thickness = 5.0
wall_thickness = 2.0
window_width = 40.0
window_height = 20.0
window_depth = 2.0
fillet_radius = 1.0
snap_thickness = 1.5
snap_height = 12.0
hinge_gap = 0.8
snap_lip_radius = 0.5

base = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_thickness)
)

base = base.edges("|Z").fillet(fillet_radius)

window_cut = (
    base.faces(">Z")
    .workplane()
    .rect(window_width, window_height)
    .cutBlind(-window_depth)
)

latch = (
    window_cut.faces(">X")
    .workplane()
    .center(0, 0)
    .rect(snap_thickness, snap_height)
    .extrude(cover_thickness)
)

latch = (
    latch.faces(">X")
    .workplane()
    .center(0, -snap_height/4)
    .rect(snap_thickness, hinge_gap)
    .cutBlind(-cover_thickness)
)

latch = latch.edges("|X").fillet(snap_lip_radius)

result = latch