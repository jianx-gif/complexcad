import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
base_thickness = 2.0
rib_height = 10.0
rib_width = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius)
rib = (
    cq.Workplane('XY')
    .circle(inner_radius)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = rib.translate((outer_radius, 0, base_thickness))
rib = rib.translate((outer_radius, 0, base_thickness))
combined = outer.union(rib)
combined = combined.faces('>Z').edges().chamfer(chamfer_distance)
combined = combined.faces('>Z').edges().chamfer(chamfer_distance)
result = combined
