import cadquery as cq
outer_diameter = 100.0
hub_radius = 12.0
rim_fillet_radius = 1.5
central_diameter = 20.0
central_fillet = 0.5
hole_diameter = central_diameter - 2 * rim_fillet
hole_count = 6
hole_spacing = (outer_diameter - inner_diameter) / 2.0
hole_spacing = (inner_diameter - inner_diameter) / 2.0
hole_positions = [(0, 0), (0, hole_spacing)]
hub = cq.Workplane('XY').circle(hub_radius).extrude(hub_height)
hub = hub.faces('>Z').workplane().circle(hub_radius).extrude(hub_height)
hub = hub.faces('>Z').edges().fillet(rim_fillet)
hub = hub.faces('>Z').edges().chamfer(rim_fillet)
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
for x, y in hole_positions:
    hub = hub.faces('>Z').workplane().pushPoints(hole_positions).circle(hole_diameter/2).extrude(hub_height)
    hub = hub.cut(hole_positions)
result = hub
