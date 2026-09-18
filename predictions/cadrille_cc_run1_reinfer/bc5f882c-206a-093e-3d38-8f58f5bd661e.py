import cadquery as cq
outer_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_width = 12.0
rib_height = 6.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .hole(inner_radius * 2)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
combined = base.union(rib)
combined = combined.edges('|Z').chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().rect(rib_width, rib_height).extrude(wall_thickness)
combined = combined.edges('>Z').chamfer(chamfer_size)
result = combined
