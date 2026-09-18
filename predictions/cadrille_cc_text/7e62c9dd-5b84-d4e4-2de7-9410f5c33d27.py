import cadquery as cq
arm_length = 80.0
outer_radius = 25.0
shell_thickness = 2.0
rib_width = 5.0
rib_height = 4.0
pivot_hole_diameter = 6.0
mount_hole_diameter = 4.0
chamfer_dist = 0.5
rib_count = 6
rib_length = arm_length - 2 * shell_thickness
rib_height = arm_length - 2 * shell_thickness
outer_radius = outer_radius - 5.0
inner_radius = outer_radius - 2.0
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, shell_thickness)
    .lineTo(inner_radius, shell_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
base = base.cut(inner_radius)
rib = (
    cq.Workplane("XY")
    .circle(rib_width / 2)
    .extrude(rib_height)
    .translate((0, 0, shell_thickness))
)
base = base.union(rib)
base = base.faces(">Z").edges().chamfer(chamfer_dist)
base = base.faces(">Z").edges().chamfer(chamfer_dist)
result = base
