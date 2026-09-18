import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
thickness = 5.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
chamfer_size = 1.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(thickness)
rib = outer_cyl.cut(inner_cyl)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_spacing, count=rib_count, startAngle=0, angle=360).hole(rib_height)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_spacing, startAngle=0, angle=360).hole(rib_height)
result = rib
