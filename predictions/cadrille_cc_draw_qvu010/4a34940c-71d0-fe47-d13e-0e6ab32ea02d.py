import cadquery as cq
outer_radius = 30.0
inner_radius = 25.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
rib_thickness = 2.0
rib_height = 5.0
rib_spacing = 12.0
chamfer_size = 0.5
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(outer_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
rib = outer_cyl.cut(inner_cyl)
rib = rib.translate((inner_radius, 0, 0))
rib = rib.translate((inner_radius, 0, 0))
rib = rib.translate((inner_radius, 0, 0))
rib = rib.translate((inner_radius, 0, 0))
combined = outer_cyl.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
rib = (
    combined.faces('>Z')
    .workplane()
    .polarArray(radius=inner_radius, startAngle=0, angle=360, count=rib_spacing)
    .hole(inner_radius * 2)
)
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
combined = combined.union(rib)
result = combined
