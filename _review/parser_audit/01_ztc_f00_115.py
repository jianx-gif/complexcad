import cadquery as cq

overall_length = 90.0
height_increment = 10.0
outer_radii = [15.0, 14.0, 13.0, 13.0, 14.0, 15.0]

profile = cq.Workplane('XY').circle(outer_radii[0])
for i in range(1, len(outer_radii)):
    profile = profile.workplane(offset=height_increment).circle(outer_radii[i])

housing = profile.loft(combine=True)

bore_diameter = 12.0
housing = housing.faces('>Z').hole(bore_diameter)

port_diameter = 4.0
chamfer_size = 0.5

for idx in [1, 3, 5]:
    radius_at_z = outer_radii[idx]
    wall_thickness = radius_at_z - bore_diameter / 2.0
    port_center_radius = bore_diameter / 2.0 + wall_thickness / 2.0
    housing = (
        housing.workplane(offset=idx * height_increment)
        .transformed(rotate=(0, 90, 0))
        .circle(port_diameter / 2.0)
        .polarArray(radius=port_center_radius, count=6, startAngle=0, angle=360)
        .hole(port_diameter)
    )

housing = housing.faces('>Z').edges().chamfer(chamfer_size)

result = housing