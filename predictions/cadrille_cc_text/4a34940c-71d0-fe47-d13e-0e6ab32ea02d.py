import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
rim_chamfer = 2.0
sensor_hole_diameter = 8.0
sensor_hole_depth = 30.0
rib_height = 12.0
rib_width = 4.0
rib_count = 6
rib_spacing = (outer_radius - wall_thickness - 1.0) / rib_count
outer_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rim_chamfer)
)
housing = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rim_chamfer)
    .translate((0, 0, -housing_height / 2))
)
housing = housing.cut(inner)
housing = housing.edges().chamfer(rim_chamfer)
housing = (
    housing.faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius - wall_thickness / 2, startAngle=0, count=4, angle=360)
    .hole(sensor_hole_diameter)
)
housing = housing.edges().chamfer(rim_chamfer)
result = housing
