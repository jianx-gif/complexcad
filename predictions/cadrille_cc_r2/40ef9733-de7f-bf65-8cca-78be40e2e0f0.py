import cadquery as cq
outer_radius = 45
inner_radius = outer_radius - inner_radius
height = 30
wall_thickness = 2
chamfer_distance = 1
hole_diameter = 5
hole_spacing = 12
hole_count = 6
hole_count = 6
hole_radius = hole_diameter / 2
hole_offset = height / 2
chamfer_distance = 1
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
result = base.cut(inner)
result = result.edges().chamfer(chamfer_distance)
hole_points = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
]
result = result.faces('>Z').workplane().pushPoints(hole_points).hole(hole_diameter)
result = result.faces('>Z').workplane().pushPoints(hole_points).hole(hole_diameter)
