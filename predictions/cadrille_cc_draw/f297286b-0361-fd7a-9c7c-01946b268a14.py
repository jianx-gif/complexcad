import cadquery as cq
outer_diameter = 100
inner_diameter = 30
thickness = 5
rib_width = 4
rib_height = 2
rib_spacing = 12
rib_count = 6
chamfer_size = 0.5
hole_diameter = 6
hole_spacing = 20
hole_count = 4
hole_radius = inner_diameter / 2 - 5
hole_offset = 15
base = cq.Workplane('XY').circle(outer_diameter / 2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .circle(outer_diameter / 2)
    .extrude(thickness)
    .translate((0, 0, thickness))
)
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
combined = combined.faces('>Z').workplane().hole(hole_diameter)
result = combined
