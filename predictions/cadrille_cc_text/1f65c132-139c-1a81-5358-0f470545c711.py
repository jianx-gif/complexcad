import cadquery as cq
cover_length = 80.0
cover_width = 60.0
cover_thickness = 5.0
wall_thickness = 2.0
pin_width = 40.0
pin_height = 20.0
pin_depth = 2.0
fillet_radius = 1.0
snap_lip_radius = 0.5
snap_lip_height = 12.0
snap_height = 12.0
hole_spacing = (cover_length - 2 * wall_thickness - 1) * hole_spacing
hole_positions = [(0, 0), (0, 0), (0, 0), (1, 0), (1, 0)]), (0, 0)]), (0, 0)])])
result = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(snap_lip_radius, snap_lip_height)
    .cutBlind(-cover_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(snap_lip_radius, snap_height)
    .cutBlind(-cover_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(snap_lip_radius, snap_lip_height)
    .cutBlind(-cover_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(snap_lip_radius, snap_height)
    .extrude(-snap_depth)
    .edges("|Z")
    .fillet(fillet_radius)
)
