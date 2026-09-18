import cadquery as cq

outer_radius = 30.0
inner_radius = 15.0
housing_length = 60.0
wall_thickness = outer_radius - inner_radius
pocket_width = 12.0
pocket_height = 30.0
pocket_depth = wall_thickness - 2.0
pocket_center_z = housing_length / 2.0
chamfer_size = 0.8
mount_hole_dia = 4.0
mount_hole_spacing = 20.0
mount_hole_offset_z = 10.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, housing_length)
    .lineTo(inner_radius, housing_length)
    .close()
)

housing = profile.revolve()

pocket = (
    cq.Workplane("XY")
    .box(pocket_depth, pocket_width, pocket_height)
    .translate((outer_radius - pocket_depth / 2.0, 0, pocket_center_z))
)

housing = housing.cut(pocket)

housing = housing.faces(">Z").edges().chamfer(chamfer_size)

hole_positions = [
    (-mount_hole_spacing / 2.0, mount_hole_offset_z),
    (mount_hole_spacing / 2.0, mount_hole_offset_z),
]

housing = (
    housing.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_dia)
)

result = housing