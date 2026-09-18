import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 10.0
rib_width = 8.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
rib_offset = 5.0
chamfer_size = 1.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = (
    combined.faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
combined = combined.union(rib)
combined = (
    combined.faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
combined = combined.union(rib)
result = combined
