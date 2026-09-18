import cadquery as cq
outer_diameter = 60.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 3.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.faces(">Z").workplane().hole(inner_diameter)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.edges().chamfer(chamfer_size)
result = base
