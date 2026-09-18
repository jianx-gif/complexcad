import cadquery as cq

outer_diameter = 80
inner_diameter = 30
retainer_thickness = 12
flange_thickness = 6
chamfer_size = 2
mount_hole_diameter = 5
mount_hole_count = 4
mount_hole_radius = (outer_diameter / 2) - 10
bearing_seat_diameter = 36
bearing_seat_depth = 8
inner_clearance_radius = (inner_diameter / 2) - 4
inner_clearance_depth = 3

inner_radius = inner_diameter / 2
outer_radius = outer_diameter / 2

top_z = retainer_thickness + flange_thickness

profile_points = [
    (inner_radius, 0),
    (inner_radius, retainer_thickness),
    (outer_radius, retainer_thickness),
    (outer_radius, top_z),
    (0, top_z),
    (0, 0)
]

result = (
    cq.Workplane("XY")
    .polyline(profile_points)
    .close()
    .revolve(360)
    .workplane(offset=top_z)
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_diameter)
    .workplane(offset=top_z)
    .center(0, 0)
    .circle(bearing_seat_diameter / 2)
    .cutBlind(bearing_seat_depth)
    .edges("|Z")
    .chamfer(chamfer_size)
    .workplane(offset=top_z)
    .circle(inner_clearance_radius)
    .cutBlind(inner_clearance_depth)
)
