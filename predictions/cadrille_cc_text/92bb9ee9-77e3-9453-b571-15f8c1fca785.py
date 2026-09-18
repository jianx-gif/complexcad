import cadquery as cq
cap_outer_radius = 45.0
cap_height = 30.0
wall_thickness = 5.0
top_chamfer = 2.0
rib_height = 5.0
rib_thickness = 2.0
rib_base_height = 10.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset = 5.0
base_chamfer = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(cap_outer_radius, 0)
    .lineTo(cap_outer_radius, cap_height - rib_height)
    .lineTo(rib_base_height, cap_height - rib_height)
    .lineTo(rib_base_height, cap_height)
    .lineTo(0, cap_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(top_chamfer)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
solid = solid.faces(">Z").edges().chamfer(top_chamfer)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_height, rib_base_height)
    .translate((0, 0, rib_base_height / 2))
)
solid = solid.union(rib)
result = solid
