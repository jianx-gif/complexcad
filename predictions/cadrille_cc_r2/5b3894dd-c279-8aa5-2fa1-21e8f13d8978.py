import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_depth = 12.0
hole_spacing = 15.0
hole_offset = 15.0
chamfer_distance = 1.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
inner_cut = cq.Workplane('XY').circle(inner_diameter/2).extrude(thickness)
result = base.cut(inner_cut)
result = result.edges().chamfer(chamfer_distance)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (hole_offset, -hole_offset),
    (0, hole_offset),
    (0, -hole_offset),
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
