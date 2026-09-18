import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 8
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_offset = 10.0
base = cq.Workplane('XY').rect(outer_diameter, outer_diameter).extrude(thickness)
inner_cyl = cq.Workplane('XY').circle(inner_diameter/2).extrude(thickness)
base = base.cut(inner_cyl)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(thickness)
    .translate((0, 0, rib_offset))
)
base = base.union(rib)
base = base.edges('|Z').chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset + hole_offset),
    (-hole_spacing/2, hole_offset + hole_offset),
    (hole_spacing/2, hole_offset + hole_offset)
]
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
base = base.faces('>Z').workplane().center(hole_spacing/2, hole_offset + hole_offset).hole(hole_diameter)
base = base.faces('>Z').workplane().center(hole_spacing/2, hole_offset).hole(hole_diameter)
base = base.edges('>Z').chamfer(chamfer_size)
result = base
