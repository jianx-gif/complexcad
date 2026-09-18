import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 7.0
rib_height = 2.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
rib_count = 8
rib_margin = 5.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = cq.Workplane('XY').circle(inner_diameter/2).extrude(thickness)
rib = rib.translate((outer_diameter/2 - rib_margin, 0, 0))
rib = rib.translate((outer_diameter/2 - rib_margin, 0, 0))
combined = base.union(rib)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().polarArray(radius=outer_diameter/2 + rib_margin, startAngle=0, angle=360, count=rib_count).rect(rib_width, rib_height).extrude(rib_width)
combined = combined.union(rib)
result = combined
