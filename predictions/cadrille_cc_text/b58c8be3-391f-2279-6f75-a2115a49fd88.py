import cadquery as cq
housing_height = 70.0
outer_radius = 30.0
inner_radius = 12.0
bearing_seat_radius = 14.0
bearing_seat_depth = 5.0
bearing_seat_height = housing_height - 2 * bearing_seat_depth
bearing_seat_radius = bearing_seat_radius - bearing_seat_depth
mount_hole_diameter = 4.0
mount_hole_radius = 22.0
rib_thickness = 3.0
rib_height = 20.0
rib_length = housing_height - 2 * bearing_seat_depth
fillet_radius = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, housing_height)
    .lineTo(inner_radius, housing_height)
    .lineTo(inner_radius, 0)
    .close()
)
housing = profile.revolve()
housing = housing.edges().fillet(fillet_radius)
bearing = (
    housing.faces(">Z").workplane()
    .center(outer_radius - bearing_seat_radius, 0)
    .rect(bearing_seat_radius, bearing_seat_height)
    .extrude(bearing_seat_depth)
)
housing = housing.faces(">Z").edges().fillet(fillet_radius)
result = housing
