import cadquery as cq
sleeve_outer_dia = 60.0
sleeve_inner_dia = 40.0
sleeve_length = 30.0
base_width = 80.0
base_thickness = 10.0
fillet_radius = 2.0
chamfer_dist = 1.0
mount_hole_dia = 5.0
mount_hole_offset = 20.0
rib_width = 8.0
rib_height = 6.0
rib_count = 4
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(sleeve_outer_dia / 2, 0)
    .lineTo(sleeve_outer_dia / 2, base_thickness)
    .lineTo(sleeve_inner_dia / 2, base_thickness)
    .lineTo(sleeve_inner_dia / 2, base_thickness + base_thickness)
    .lineTo(sleeve_inner_dia / 2, base_thickness + base_thickness + base_thickness)
    .lineTo(sleeve_inner_dia / 2, base_thickness + base_thickness + base_thickness + base_thickness)
    .lineTo(sleeve_inner_dia / 2, base_thickness + base_thickness + base_thickness + base_thickness + base_thickness + base_thickness + base_thickness + 2)
    .lineTo(sleeve_inner_dia / 2, base_thickness + base_thickness + base_thickness + 2)
    .lineTo(sleeve_outer_dia / 2, base_thickness + base_thickness + 2)
    .close()
    .revolve(360)
)
base = (
    cq.Workplane("XY")
    .box(base_width, base_thickness, base_thickness + 2)
    .translate((sleeve_outer_dia / 2 - base_thickness / 2, 0, 0))
)
base = base.union(base)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_height)
    .translate((sleeve_outer_dia / 2 - rib_width / 2, 0, base_thickness + base_thickness + rib_height / 2))
)
result = base.union(rib)
