import cadquery as cq
outer_diameter = 80.0
hub_diameter = 30.0
hub_width = 12.0
wall_thickness = 4.0
keyway_width = 6.0
keyway_depth = 5.0
keyway_depth = 4.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
hub_radius = hub_diameter / 2.0
hub_radius = hub_radius + hub_width
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(hub_width)
inner_cyl = cq.Workplane('XY').circle(hub_radius).extrude(hub_width)
hub = cq.Workplane('XY').circle(hub_radius).extrude(hub_width)
hub = hub.cut(inner_cyl)
hub = hub.faces('>Z').workplane().hole(shaft_diameter)
result = hub.union(hub)
result = result.edges().chamfer(chamfer_size)
result = result.faces('>Z').workplane().hole(keyway_depth)
result = result.faces('>Z').workplane().polarArray(radius=hub_radius, count=6, startAngle=0, angle=360).hole(keyway_depth)
result = result.faces('>Z').workplane().polarArray(radius=hub_radius - wall_thickness/2, count=6, startAngle=0, angle=360).circle(hub_radius).cutBlind(-hub_width)
