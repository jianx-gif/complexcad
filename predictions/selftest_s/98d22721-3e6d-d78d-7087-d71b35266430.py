import cadquery as cq

gusset_width = 60.0
gusset_height = 40.0
gusset_thickness = 8.0
corner_radius = 10.0
mount_hole_diameter = 8.0
counterbore_diameter = 12.0
counterbore_depth = 4.0
mount_hole_offset_x = 20.0
mount_hole_offset_y = 15.0
chamfer_size = 1.0
rib_width = 20.0
rib_height = 5.0
rib_depth = 3.0
rib_offset_y = 5.0

base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(gusset_width, 0)
    .lineTo(gusset_width, gusset_height - corner_radius)
    .threePointArc((gusset_width, gusset_height), (gusset_width - corner_radius, gusset_height))
    .lineTo(0, gusset_height)
    .close()
    .extrude(gusset_thickness)
)

with_hole = (
    base
    .faces(">Z")
    .workplane()
    .moveTo(mount_hole_offset_x, mount_hole_offset_y)
    .cboreHole(mount_hole_diameter, counterbore_diameter, counterbore_depth)
)

rib_cut = (
    with_hole
    .faces("<Z")
    .workplane()
    .moveTo(gusset_width/2, rib_offset_y)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_depth)
)

result = (
    rib_cut
    .edges("|Z")
    .chamfer(chamfer_size)
)
