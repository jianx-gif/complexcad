import cadquery as cq

base_width = 80.0
base_depth = 30.0
base_thickness = 5.0
base_corner_radius = 0.8
clip_arm_length = 40.0
clip_arm_width = 12.0
clip_arm_thickness = 3.0
clip_hole_diameter = 8.0
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
rib_width = 2.0
rib_height = 4.0
rib_depth = 2.0
rib_spacing = 6.0
rib_chamfer = 0.5

rib_count = int(clip_arm_length // rib_spacing)

base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
    .faces(">Z")
    .tag("base_top")
)

result = (
    base
    .workplaneFromTagged("base_top")
    .center(0, -base_depth/2 - clip_arm_width/2)
    .rect(clip_arm_length, clip_arm_width)
    .extrude(clip_arm_thickness)
    .faces(">Y")
    .tag("clip_front")
    .workplaneFromTagged("base_top")
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .circle(mount_hole_diameter/2)
    .cutBlind(base_thickness)
    .workplaneFromTagged("clip_front")
    .center(0, 0)
    .circle(clip_hole_diameter/2)
    .cutBlind(clip_arm_thickness)
    .faces(">Y")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1, center=True)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
    .edges(">Y")
    .chamfer(rib_chamfer)
)
