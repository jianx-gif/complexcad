import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 5.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
