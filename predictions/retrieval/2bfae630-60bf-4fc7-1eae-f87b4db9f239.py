import cadquery as cq

rail_total_length = 80
nose_length = 12
outer_radius = 20
thickness = 5
inner_radius = outer_radius - thickness
fillet_radius = 2
bearing_seat_radius = 8
bearing_seat_depth = 4
bearing_seat_center_z = rail_total_length / 2
mount_hole_dia = 4
mount_hole_offset_z = 20

profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (outer_radius, nose_length),
        (outer_radius, rail_total_length),
        (0, rail_total_length),
    ])
    .close()
)

solid = profile.revolve()

hollow = solid.shell(thickness)

bearing_cylinder = (
    cq.Workplane()
    .circle(bearing_seat_radius)
    .extrude(bearing_seat_depth)
    .translate((outer_radius - bearing_seat_depth / 2, 0, bearing_seat_center_z))
)

hole_cylinder = (
    cq.Workplane()
    .circle(mount_hole_dia / 2)
    .extrude(outer_radius * 2)
    .translate((outer_radius - thickness / 2, 0, mount_hole_offset_z))
)

intermediate = hollow.cut(bearing_cylinder).cut(hole_cylinder)

result = intermediate.edges("|Z").fillet(fillet_radius)