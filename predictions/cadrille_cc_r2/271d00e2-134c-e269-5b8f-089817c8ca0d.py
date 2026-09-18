import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 12
hole_count = 4
hole_spacing = 12.0
hole_offset = 10.0
chamfer_distance = 1.0
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius).translate((0, 0, wall_thickness))
inner = inner.cut(inner)
result = inner
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    rotated = inner.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated)
result = result.edges().chamfer(chamfer_distance)
result = result.faces('>Z').workplane().hole(hole_diameter)
result = result.faces('>Z').workplane().hole(hole_diameter)
