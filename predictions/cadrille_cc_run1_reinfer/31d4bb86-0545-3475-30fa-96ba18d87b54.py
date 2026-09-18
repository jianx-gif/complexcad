import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
base = base.cut(inner)
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_height)
       .extrude(wall_thickness))
base = base.union(rib)
base = base.edges('|Z').chamfer(chamfer_distance)
base = base.edges('>Z').fillet(inner_radius)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().hole(inner_radius * 2, inner_radius * 2, inner_radius * 2))
base = base.faces('>Z').workplane().hole(hole_diameter)
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_height)
       .extrude(wall_thickness))
rib = rib.union(rib)
result = base.union(rib)
