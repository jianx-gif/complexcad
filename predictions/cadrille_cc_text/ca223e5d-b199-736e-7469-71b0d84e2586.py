import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_cyl = cq.Workplane('XZ').cylinder(outer_radius, outer_radius)
inner_cyl = cq.Workplane('XZ').cylinder(outer_radius, inner_radius)
rib_width = 5.0
rib_height = 70.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_count = 6
hole_spacing = (outer_radius - wall_thickness - 1.0) / (hole_count - 1)
hole_positions = [(hole_count - 1) * hole_spacing, hole_count - 1) * hole_spacing]
for i in range(hole_count):
    z = i * hole_spacing
    hole_positions.append((x, z))
inner_cyl = cq.Workplane('XY').cylinder(outer_radius - wall_thickness - 2.0, inner_radius - wall_thickness - 2.0)
inner_cyl = cq.Workplane('XY').cylinder(outer_radius - wall_thickness - 2.0, inner_radius - wall_thickness - 2.0)
inner_cyl = inner_cyl.cut(inner_cyl)
result = outer_cyl.cut(inner_cyl)
result = result.faces('>Z').edges().chamfer(chamfer_distance)
