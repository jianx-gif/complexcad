import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 3.0
inner_radius = inner_radius + wall_thickness
base_thickness = 5.0
base_height = 10.0
chamfer_size = 0.5
rib_width = 4.0
rib_height = 2.0
rib_spacing = 12.0
rib_count = 4
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(base_thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
base = outer_cyl.cut(inner_cyl)
rib = (
    cq.Workplane('XY')
    .center(inner_radius + rib_spacing / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height))
rib = rib.translate((0, 0, base_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height + rib_height))
rib = rib.translate((0, 0, base_height + rib_height + rib_height))
result = rib.union(rib)
