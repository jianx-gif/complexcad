import cadquery as cq
outer_diameter = 90.0
inner_diameter = 60.0
thickness = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_radius = inner_diameter/2 - rib_width/2
rib_count = 3
rib_spacing = 15.0
rib_height = 5.0
rib_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(outer_diameter/2 - rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((outer_diameter/2 - rib_offset, 0, 0))
rib = rib.translate((outer_diameter/2 - rib_offset, 0, 0))
rib = rib.translate((outer_diameter/2 - rib_offset, 0, 0))
rib = rib.translate((outer_diameter/2 - rib_offset, 0, 0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(rib_radius)
combined = combined.faces('>Z').workplane().hole(rib_count)
result = combined
