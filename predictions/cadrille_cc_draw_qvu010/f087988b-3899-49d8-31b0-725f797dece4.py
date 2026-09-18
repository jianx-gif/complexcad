import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(thickness)
rib = outer_cyl.cut(inner_cyl)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_width)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, count=rib_count, startAngle=0, angle=360).hole(rib_height)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360).hole(rib_height)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360).hole(rib_height)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360).rect(rib_width, rib_height).extrude(rib_width)
result = rib
