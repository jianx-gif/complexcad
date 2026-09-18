import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
height = 70.0
wall_thickness = 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_offset = height / 2.0
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = inner_cyl.cut(inner_cyl)
hole_positions = [(-hole_offset, hole_offset), (hole_offset, hole_offset), (hole_offset, hole_offset)]
for pos in hole_positions:
    inner_cyl = inner_cyl.union(hole_positions)
result = inner_cyl.cut(hole_positions)
