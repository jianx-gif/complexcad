import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 5.0
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_count = 6
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
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().hole(inner_diameter)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_thickness/2, count=rib_count, startAngle=0, angle=360).hole(rib_thickness)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_thickness/2, startAngle=0, angle=360).hole(rib_thickness)
rib = rib.faces('>Z').workplane().polarArray(radius=outer_radius - rib_thickness/2, startAngle=0, angle=360).hole(rib_count)
result = rib
