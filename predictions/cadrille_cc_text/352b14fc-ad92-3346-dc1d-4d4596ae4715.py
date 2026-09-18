import cadquery as cq
outer_radius = 40.0
inner_radius_inlet = 12.0
length = 80.0
flange_thickness = 8.0
flange_diameter = 70.0
flange_thickness = 4.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
chamfer_size = 1.0
clip_width = 20.0
clip_height = 6.0
clip_thickness = 4.0
outer_radius = outer_radius_inlet - inner_radius_outlet
inner_radius = inner_radius_inlet - inner_radius_outlet
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(length)
)
flange = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(length)
)
clip = (
    cq.Workplane("XY")
    .box(clip_width, clip_thickness, length)
    .translate((0, 0, length))
)
clip = clip.cut(clip)
clip = clip.edges("|Z").chamfer(chamfer_size)
clip = clip.edges(">Z").chamfer(chamfer_size)
clip = clip.faces(">Z").workplane().hole(mount_hole_diameter)
clip = clip.faces(">Z").workplane().hole(mount_hole_diameter)
clip = clip.edges(">Z").chamfer(chamfer_size)
clip = clip.edges(">Z").chamfer(chamfer_size)
result = clip
