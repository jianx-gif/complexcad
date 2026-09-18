import cadquery as cq
outer_radius = 45
inner_radius = 20
height = 30
wall_thickness = 2
chamfer_distance = 2
hole_diameter = 5
hole_spacing = 12
hole_count = 4
hole_spacing = 12
chamfer_distance = 2
outer = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = inner.cut(inner)
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
result = inner
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    hole = cq.Workplane('XY').circle(hole_diameter/2).extrude(hole_spacing)
    result = result.cut(hole)
