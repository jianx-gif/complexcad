import cadquery as cq
base_width = 80.0
base_depth = 30.0
base_thickness = 5.0
clip_arm_length = 40.0
clip_arm_width = 12.0
clip_arm_thickness = 3.0
base_corner_radius = 0.8
clip_hole_diameter = 8.0
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
rib_width = 2.0
rib_height = 4.0
rib_depth = 2.0
rib_chamfer = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)
clip = (
    cq.Workplane("XY")
    .rect(clip_arm_length, clip_arm_width)
    .extrude(clip_arm_thickness)
    .translate((0, 0, base_thickness))
)
clip = clip.edges("|Z").chamfer(clip_arm_thickness)
clip = clip.edges("|Z").fillet(clip_hole_diameter)
clip = clip.edges(">Z").chamfer(clip_arm_thickness)
clip = clip.edges(">Z").chamfer(clip_hole_diameter)
clip = clip.faces(">Z").workplane().center(0, 0).circle(mount_hole_diameter/2).cutBlind(-clip_arm_thickness)
result = clip
