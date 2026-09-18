import cadquery as cq
outer_radius = 50.0
hub_radius = 12.0
disc_thickness = 8.0
central_hole_diameter = 6.0
vent_ring_width = 3.0
vent_ring_spacing = 5.0
vent_ring_rows = 2
vent_ring_cols = 3
vent_ring_spacing = 5.0
chamfer_size = 0.8
outer_radius = outer_radius - hub_radius
hub_radius = 12.0
hub = cq.Workplane('XY').circle(outer_radius).extrude(disc_thickness)
hub = hub.faces('>Z').workplane().circle(hub_radius).extrude(disc_thickness)
hub = hub.faces('>Z').workplane().circle(central_hole_diameter/2).extrude(disc_thickness)
hub = hub.faces('>Z').workplane().polarArray(radius=outer_radius - vent_ring_width/2, count=vent_ring_cols, startAngle=0, angle=360).circle(central_hole_diameter/2).extrude(disc_thickness)
hub = hub.cut(hub)
vent_cut = (
    cq.Workplane('XY')
    .center(outer_radius - vent_ring_spacing/2, 0)
    .circle(vent_ring_width/2)
    .extrude(disc_thickness + 2)
)
vent_cut = (
    cq.Workplane('XY')
    .center(outer_radius - vent_ring_spacing/2, 0)
    .circle(vent_ring_width/2)
    .extrude(disc_thickness + 2)
)
hub = hub.cut(vent_cut)
hub = hub.cut(hub)
hub = hub.edges('|Z').chamfer(chamfer_size)
result = hub
