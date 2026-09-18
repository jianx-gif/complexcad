import cadquery as cq
gusset_width = 60.0
gusset_height = 40.0
gusset_thickness = 8.0
corner_radius = 10.0
mount_hole_diameter = 8.0
mount_hole_offset_x = 20.0
mount_hole_offset_y = 15.0
counterbore_diameter = 12.0
counterbore_depth = 4.0
rib_height = 5.0
rib_width = 20.0
rib_depth = 3.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(gusset_width, 0)
    .lineTo(gusset_width, gusset_height)
    .lineTo(corner_radius, gusset_height)
    .lineTo(corner_radius, gusset_height + gusset_thickness)
    .lineTo(0, gusset_height + gusset_thickness)
    .close()
    .extrude(gusset_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_depth)
    .cutBlind(-rib_depth)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .cboreHole(mount_hole_diameter, counterbore_diameter, counterbore_depth)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_depth)
    .extrude(rib_height)
)
result = base
