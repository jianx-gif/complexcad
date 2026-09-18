import cadquery as cq
outer_diameter = 60.0
height = 30.0
wall_thickness = 2.5
central_hole_diameter = 10.0
rib_width = 8.0
rib_thickness = 3.0
rib_count = 4
chamfer_dist = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
base = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
base = base.cut(inner_cyl)
rib = (cq.Workplane('XY')
       .box(rib_thickness, rib_width, rib_thickness)
       .translate((outer_radius - rib_thickness / 2.0, 0, height / 2.0)))
rib = rib.translate((0, 0, height / 2.0))
rib = rib.translate((0, 0, height / 2.0))
result = base.union(rib)
result = result.faces('>Z').edges().chamfer(chamfer_dist)
