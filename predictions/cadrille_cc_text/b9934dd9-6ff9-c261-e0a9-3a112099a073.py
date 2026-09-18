import cadquery as cq
outer_diameter = 80.0
wall_thickness = 8.0
inner_diameter = outer_diameter - 2 * wall_thickness
housing_height = 60.0
base_plate_thickness = 5.0
central_bore_diameter = 20.0
counterbore_diameter = 30.0
counterbore_depth = 15.0
chamfer_size = 2.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = outer_diameter / 2.0
base_plate_thickness = 5.0
base_plate = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, housing_height)
    .lineTo(inner_diameter / 2.0, housing_height)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
housing = base_plate.union(base_plate)
housing = housing.edges().chamfer(chamfer_size)
housing = (
    housing.faces(">Z")
    .workplane()
    .circle(counterbore_diameter / 2.0)
    .cutBlind(counterbore_depth)
)
mount_hole = (
    cq.Workplane("XY")
    .circle(mount_hole_diameter / 2.0)
    .extrude(mount_hole_radius * 2)
)
housing = housing.cut(mount_hole)
housing = housing.edges().chamfer(chamfer_size)
result = housing
