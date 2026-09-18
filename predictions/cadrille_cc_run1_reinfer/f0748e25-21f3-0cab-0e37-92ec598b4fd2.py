import cadquery as cq
outer_radius = 40.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(inner_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0,0,0))
base = base.cut(inner)
rib = cq.Workplane('XY').rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.union(rib)
rib = rib.edges().chamfer(chamfer_size)
result = base.union(rib)
