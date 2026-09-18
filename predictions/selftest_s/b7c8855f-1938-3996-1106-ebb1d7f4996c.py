import cadquery as cq

base_width = 70.0
base_depth = 30.0
base_height = 5.0
base_corner_radius = 3.0
mount_hole_dia = 6.0
mount_hole_spacing = 20.0

clip_body_width = 20.0
clip_body_height = 15.0
clip_body_thickness = 4.0
interior_fillet_radius = 2.0
slot_width = 3.0
slot_spacing = 8.0
rib_height = 3.0
rib_width = 5.0


def clip_body():
    profile = (
        cq.Workplane("XY")
        .center(-clip_body_width / 2, -clip_body_height / 2)
        .rect(clip_body_width, clip_body_height)
        .moveTo(-clip_body_width / 2, clip_body_height / 2)
        .lineTo(-clip_body_width / 2 - rib_width, clip_body_height / 2 + rib_height)
        .lineTo(clip_body_width / 2 + rib_width, clip_body_height / 2 + rib_height)
        .lineTo(clip_body_width / 2, clip_body_height / 2)
    )
    solid = profile.extrude(clip_body_thickness)
    solid = solid.edges("<Y and |Z").fillet(interior_fillet_radius * 0.99)
    return solid

base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_height)
    .edges("|Z").tag("base_edges").end()
    .faces(">Z")
    .workplane()
    .center(0, base_depth / 2 - mount_hole_spacing / 2)
    .circle(mount_hole_dia / 2)
    .cutThruAll()
    .center(0, mount_hole_spacing)
    .circle(mount_hole_dia / 2)
    .cutThruAll()
)

clip = clip_body().translate((0, -base_depth / 2 - clip_body_width / 2, base_height))

slot_positions = [-(slot_spacing / 2 + slot_width / 2), (slot_spacing / 2 + slot_width / 2)]
for x in slot_positions:
    clip = (
        clip
        .faces(">Z")
        .workplane()
        .center(x, 0)
        .rect(slot_width, clip_body_height + 2)
        .cutBlind(-clip_body_thickness - 0.2)
    )

clip = clip.edges("<<X and |Z").fillet(interior_fillet_radius)

# bridging tab to fuse base and clip
tab = (
    cq.Workplane("XY")
    .center(-clip_body_width / 2, -base_depth / 2 - 7.5)
    .rect(5, 15)
    .extrude(base_height + 0.5)
)

result = base.union(tab).union(clip)
