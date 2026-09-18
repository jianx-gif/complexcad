import cadquery as cq
import math
base_width = 60.0
base_height = 30.0
base_thickness = 5.0
wall_thickness = 2.0
rib_height = 4.0
rib_width = 8.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
base = cq.Workplane('XY').rect(base_width, base_height).extrude(base_thickness)
base = base.faces('>Z').workplane().hole(2 * base_width)
base = base.faces('>Z').workplane().hole(2 * base_thickness)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
base = base.edges('>Z').chamfer(chamfer_size)
base = base.faces('>Z').workplane().hole(2 * base_width)
base = base.faces('>Z').workplane().hole(2 * base_width)
base = base.faces('>Z').workplane().hole(2 * base_width)
base = base.faces('>Z').workplane().hole(2 * base_width)
base = base.edges().chamfer(chamfer_size)
base = base.edges().chamfer(chamfer_size)
base = base.edges().chamfer(chamfer_size)
base = base.faces('>Z').workplane().hole(2 * base_width)
base = base.faces('>Z').workplane().hole(2 * base_width)
base = base.edges().chamfer(chamfer_size)
result = base
