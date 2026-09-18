import cadquery as cq
inner_radius = 30.0
outer_radius = 40.0
height = 20.0
wall_thickness = 2.0
rib_height = 5.0
rib_radius = outer_radius - wall_thickness
rib_radius = outer_radius - wall_thickness
outer_radius = inner_radius + wall_thickness
outer_radius = outer_radius - wall_thickness
outer_cyl = cq.Workplane('XY').cylinder(height, outer_radius)
outer_cyl = cq.Workplane('XY').cylinder(height, outer_radius - wall_thickness)
outer_cyl = cq.Workplane('XY').cylinder(height, outer_radius - wall_thickness)
outer_cyl = cq.Workplane('XY').cylinder(height, outer_radius - wall_thickness)
outer_cyl = cq.Workplane('XY').cylinder(height, outer_radius - wall_thickness)
outer_cyl = cq.Workplane('XY').cylinder(height, outer_radius - wall_thickness)
outer_cyl = cq.Workplane('XY').cylinder(height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.cut(outer_cyl)
outer_cyl = outer_cyl.workplane(offset=outer_radius).hole(outer_radius * 2)
outer_cyl = outer_cyl.workplane(offset=outer_radius).hole(outer_radius * 2)
outer_cyl = outer_cyl.workplane(offset=outer_radius).hole(outer_radius * 2)
outer_cyl = outer_cyl.workplane(offset=outer_radius).cylinder(outer_radius * 2, outer_radius * 2)
outer_cyl = outer_cyl.workplane(offset=outer_radius).translate((0, 0, wall_thickness))
outer_cyl = outer_cyl.workplane(offset=outer_radius).cylinder(outer_radius * 2, outer_radius * 2)
outer_cyl = outer_cyl.workplane(offset=outer_radius).translate((0, 0, wall_thickness))
outer_cyl = outer_cyl.workplane(offset=outer_radius).polarArray(outer_radius - wall_thickness, 0, 360, 2).translate((0, 0, wall_thickness))
outer_cyl = outer_cyl.workplane(offset=outer_radius).polarArray(outer_radius - wall_thickness, 0, 360, 2).extrude(outer_radius)
result = outer_cyl.union(outer_cyl)
