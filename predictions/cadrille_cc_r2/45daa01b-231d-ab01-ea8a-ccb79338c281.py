import cadquery as cq
outer_radius = 45
inner_radius = 20
height = 30
wall_thickness = 2
chamfer_distance = 1
rib_width = 6
rib_height = 4
rib_thickness = 2
rib_spacing = 12
rib_count = 8
chamfer_distance = 1
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner_cylinder = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cylinder = cq.Workplane('XY').circle(inner_radius).extrude(height)
rib = base.cut(inner_cylinder)
rib = rib.translate((0,0,0), (0,0,1), 90))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().polarArray(radius=inner_radius - wall_thickness/2, startAngle=0, angle=360, count=rib_count).rect(rib_width, rib_height).extrude(rib_thickness)
result = combined
