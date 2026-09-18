import cadquery as cq
outer_diameter = 60.0
inner_diameter = 40.0
thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(thickness)
rib = outer_cyl.union(inner_cyl)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, count=rib_count).hole(inner_diameter)
rib = rib.faces('<Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, count=rib_count).hole(inner_diameter)
rib = rib.faces('<Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, count=rib_count).hole(inner_diameter)
rib = rib.faces('<Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, count=rib_count).hole(inner_diameter)
rib = rib.faces('<Z').edges().chamfer(chamfer_size)
rib = rib.faces('<Z').edges().chamfer(chamfer_size)
rib = rib.faces('<Z').edges().chamfer(chamfer_size)
rib = rib.faces('<Z').edges().chamfer(chamfer_size)
rib = rib.faces('<Z').edges().chamfer(chamfer_size)
rib = rib.faces('<Z').edges().chamfer(chamfer_size)
rib = rib.faces('<Z').edges().chamfer(chamfer_size)
rib = rib.faces('>>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>>Z').workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib.faces('>>Z").workplane().polarArray(radius=outer_radius - rib_width/2, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
rib = rib