import cadquery as cq
base_width = 80.0
base_depth = 40.0
base_thickness = 4.0
base_corner_radius = 5.0
rear_bevel = 1.0
rear_bevel = 2.5
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_rows = 2
mount_hole_cols = 3
mount_hole_rows = 2
mount_hole_cols = 2
mount_hole_spacing = 20.0
clip_thickness = 2.5
clip_height = 30.0
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)
clip = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(mount_hole_diameter / 2)
    .extrude(clip_thickness)
)
clip = clip.edges("|Z").chamfer(0.5)
clip = clip.edges(">Z").chamfer(clip_thickness)
clip = clip.edges(">Z").fillet(clip_height)
result = clip
