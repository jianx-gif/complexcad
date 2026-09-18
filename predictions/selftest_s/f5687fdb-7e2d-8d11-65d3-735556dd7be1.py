import cadquery as cq

total_height = 60.0
base_radius = 10.0
radial_extension = 15.0
max_radius = base_radius + radial_extension
wall_thickness = 4.0
fillet_radius = 1.0
hole_diameter = 6.0
hole_position_z = 0.0
tab_width = 20.0
tab_thickness = wall_thickness
tab_height = 8.0
chamfer_distance = 0.5

profile = (
    cq.Workplane("XY")
    .moveTo(base_radius, -total_height/2)
    .spline([
        (base_radius, -total_height/4),
        (max_radius, -total_height/8),
        (max_radius, 0),
        (max_radius, total_height/8),
        (base_radius, total_height/4),
        (base_radius, total_height/2),
    ])
    .close()
)

result = (
    profile
    .revolve()
    .shell(-wall_thickness)
    .edges().fillet(fillet_radius)
    .cut(
        cq.Workplane("XY")
        .center(base_radius + wall_thickness/2, hole_position_z)
        .transformed(rotate=cq.Vector(0, 90, 0))
        .circle(hole_diameter/2)
        .extrude(wall_thickness*2 + 10)
    )
    .workplane(offset=-total_height/2)
    .rect(tab_width, tab_thickness)
    .extrude(tab_height)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
