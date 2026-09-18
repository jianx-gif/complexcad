import cadquery as cq
import math
length = 80
width_top = 30
width_bottom = 20
height = 20
thickness = 6
groove_depth = 2
groove_angle = 60
groove_half_width = groove_depth / math.tan(math.radians(groove_angle / 2))
hole_diameter = 4
hole_depth = 5
hole_spacing = 12
edge_margin = thickness + 2
rib_width = thickness / 2
rib_height = height / 4
rib_length = length / 4
rib_positions_z = [length * 0.2, length * 0.5, length * 0.8]
outer = (
    cq.Workplane()
    .rect(width_top, height)
    .workplane(offset=length)
    .rect(width_bottom, height)
    .loft()
)
combined = outer
for z in rib_positions_z:
    rib = (
        cq.Workplane('XY')
        .center(width_top / 2 - thickness - rib_width / 2, 0)
        .rect(rib_width, rib_height)
        .extrude(rib_length)
        .translate((0, 0, z - rib_length / 2))
    )
    combined = combined.union(rib)
# tab
tab_length = 10
tab_overlap = 1
tab = (
    cq.Workplane('XY')
    .center(width_top / 2 - tab_overlap / 2, -height / 2 + thickness / 2)
    .rect(tab_length, thickness)
    .extrude(thickness)
)
combined = combined.union(tab)
inner = (
    cq.Workplane()
    .rect(width_top - 2 * thickness, height - 2 * thickness)
    .workplane(offset=length)
    .rect(width_bottom - 2 * thickness, height - 2 * thickness)
    .loft()
)
result = combined.cut(inner)
# groove
groove = (
    cq.Workplane('XY')
    .center(width_top / 2, 0)
    .polyline([
        (0, 0),
        (-groove_depth, -groove_half_width),
        (-groove_depth, groove_half_width),
        (0, 0)
    ])
    .close()
    .extrude(length)
)
result = result.cut(groove)
# holes
hole_positions = []
for i in range(3):
    for j in range(2):
        x = -width_top / 2 + edge_margin + i * hole_spacing
        y = -height / 2 + edge_margin + j * hole_spacing
        hole_positions.append((x, y))
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)
