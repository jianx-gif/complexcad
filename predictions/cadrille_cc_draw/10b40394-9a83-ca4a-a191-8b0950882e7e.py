import cadquery as cq
outer_diameter = 80.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(wall_thickness)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(wall_thickness)
)
base = base.cut(inner_cyl)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
result = base
