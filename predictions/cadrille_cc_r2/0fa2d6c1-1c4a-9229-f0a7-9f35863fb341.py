import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 80
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
base_thickness = 10
base_height = 15
chamfer_size = 1
hole_diameter = 5
hole_spacing = 30
hole_count = 6
hole_count = 4
hole_spacing = hole_spacing / 2
hole_spacing = hole_spacing / 2
outer = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = inner.cut(inner)
result = inner
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    rotated = inner.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated)
result = result.edges().chamfer(chamfer_size)
