import cadquery as cq
housing_length = 100.0
inlet_radius = 12.0
wall_thickness = 2.0
fillet_radius = 0.8
vent_hole_diameter = 3.0
vent_spacing = 8.0
vent_rows = 2
vent_cols = 3
vent_hole_radius = inlet_radius + wall_thickness/2
outer_radius = inlet_radius + wall_thickness/2
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(inlet_radius)
inner_cyl = cq.Workplane('XY').circle(inner_cyl).extrude(inlet_radius)
result = outer_cyl.cut(inner_cyl)
result = result.faces('>Z').workplane().hole(vent_hole_diameter)
result = result.faces('>Z').edges().fillet(fillet_radius)
