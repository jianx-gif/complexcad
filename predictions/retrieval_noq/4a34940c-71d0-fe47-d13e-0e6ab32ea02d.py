import cadquery as cq

outer_radius = 45
height = 60
wall_thickness = 12
inner_radius = outer_radius - wall_thickness
vent_width = 20
vent_height = 30
vent_offset = 10
fillet_radius = 3

profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
)

housing = profile.revolve(360)

vent_cut = (
    cq.Workplane('XZ')
    .center(outer_radius - wall_thickness/2, vent_offset)
    .rect(vent_width, vent_height)
    .extrude(wall_thickness * 2)
)

housing = housing.cut(vent_cut)

housing = housing.edges('>Z').fillet(fillet_radius)

result = housing