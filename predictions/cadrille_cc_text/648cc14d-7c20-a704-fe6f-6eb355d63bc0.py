import cadquery as cq
base_width = 80.0
base_height = 30.0
base_thickness = 8.0
base_corner_radius = 3.0
slot_width = 4.0
slot_length = 20.0
slot_spacing = 6.0
clip_thickness = 3.0
clip_height = 25.0
clip_radius = 5.0
clip_thickness = 3.0
chamfer_dist = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(clip_radius)
    .cutBlind(clip_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
    .edges("|Z")
    .chamfer(chamfer_dist)
)
clip = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(clip_thickness, clip_height)
    .extrude(clip_thickness)
    .edges("|Z")
    .fillet(clip_radius)
)
clip = clip.edges("|Z").chamfer(chamfer_dist)
clip = clip.edges("|Z").fillet(clip_thickness)
result = base.union(clip)
