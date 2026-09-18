import cadquery as cq
outer_width = 50.0
outer_height = 40.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
base = cq.Workplane('XY').rect(outer_width, outer_height).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(rib_width)
combined = combined.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-thickness)
combined = combined.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-thickness)
combined = combined.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-thickness)
result = combined
