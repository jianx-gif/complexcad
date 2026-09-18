import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 6.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
rib = base.faces('>Z').workplane().hole(inner_radius * 2)
rib = rib.translate((0, 0, rib_height))
rib = rib.translate((0, 0, rib_height))
result = base.union(rib)
