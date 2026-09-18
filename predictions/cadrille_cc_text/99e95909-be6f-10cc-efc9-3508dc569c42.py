import cadquery as cq
base_width = 80.0
base_depth = 40.0
base_height = 5.0
base_corner_radius = 3.0
base_corner_length = 30.0
rib_width = 4.0
rib_height = 2.0
rib_spacing = 10.0
clip_arm_length = 30.0
clip_flex_radius = 8.0
clip_flex_height = 12.0
fillet_radius = 0.8
chamfer_size = 1.0
pilot_hole_diameter = 3.0
pilot_hole_count = 4
pilot_hole_radius = pilot_hole_diameter / 2.0
rib_count = int((base_width - 2 * rib_spacing) // rib_spacing) + 1
rib_length = base_width - 2 * rib_spacing
rib_length = base_depth - 2 * rib_spacing
rib_width = base_width - 2 * rib_spacing
rib_height = 2.0
rib_spacing = rib_length / rib_count
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_height)
    .edges("|Z")
    .fillet(fillet_radius)
)
clip = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(clip_arm_length)
    .extrude(clip_flex_height)
    .translate((0, 0, base_height))
)
clip = clip.union(clip)
clip = (
    clip
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
clip = clip.edges("|Z").fillet(fillet_radius)
result = base.union(clip)
