import cadquery as cq
panel_width = 80
panel_height = 60
panel_thickness = 4
rib_width = 30
rib_height = 8
rib_thickness = 2
hole_diameter = 4
hole_depth = 2.5
hole_spacing = 12
hole_count = 5
fillet_radius = 0.5
base = cq.Workplane('XY').box(panel_width, panel_height, panel_thickness)
rib = base.faces('>Z').workplane().center(panel_width/2 - rib_width/2, 0).rect(rib_width, rib_height).extrude(rib_thickness)
result = base.union(rib)
result = result.faces('>Z').workplane().center(-panel_width/2 + 10, 0).rarray(hole_spacing, 0, hole_count, 1).circle(hole_diameter/2).cutBlind(hole_depth)
result = result.edges('|Z').fillet(fillet_radius)
