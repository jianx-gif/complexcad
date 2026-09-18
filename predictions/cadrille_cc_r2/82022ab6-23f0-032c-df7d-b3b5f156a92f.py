import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
boss_radius = 10.0
boss_height = 12.0
boss_depth = 5.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 30.0
hole_count = 12
hole_count = 6
hole_count = 12
hole_spacing = 15.0
hole_offset = 10.0
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = inner.cut(inner)
hole_positions = [
    (hole_count - 1) * hole_spacing, hole_count - 1),
    (hole_count - 1) * hole_spacing, hole_count - 1)
]
result = inner
for i in range(hole_count):
    for j in range(hole_count):
        x = hole_spacing * math.cos(2 * math.pi * i / hole_count
        y = hole_spacing * math.sin(2 * math.pi * i / hole_count
        hole_positions.append((x, y))
result = result.cut(hole_positions)
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
