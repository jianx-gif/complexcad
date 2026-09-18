import cadquery as cq
outer_radius = 45.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_count = 3
hole_count = 2
hole_spacing = 30.0
rib_width = 10.0
rib_height = 5.0
rib_thickness = 2.0
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
base = base.cut(inner)
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_height)
       .translate((outer_radius - rib_thickness/2, 0, 0))
       .extrude(wall_thickness))
combined = base.union(rib)
combined = combined.edges('|Z').chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.edges('>Z').chamfer(chamfer_size)
result = combined
