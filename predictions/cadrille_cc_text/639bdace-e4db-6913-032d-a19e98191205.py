import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
housing_length = 40.0
flange_extra_radius = 15.0
flange_height = 10.0
sensor_pocket_width = 12.0
sensor_pocket_height = 8.0
sensor_pocket_depth = 6.0
sensor_pocket_offset = 20.0
chamfer_size = 1.5
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
rib_thickness = 2.0
rib_height = 6.0
rib_spacing = 10.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - flange_extra_radius
result = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, housing_length - flange_height)
    .lineTo(inner_radius + flange_extra_radius, housing_length - flange_height)
    .lineTo(inner_radius + flange_extra_radius, housing_length)
    .lineTo(inner_radius, housing_length)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
    .edges()
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (mount_hole_spacing / 2, mount_hole_spacing / 2),
        (mount_hole_spacing / 2, mount_hole_spacing / 2),
        (mount_hole_spacing / 2, mount_hole_spacing / 2),
        (mount_hole_spacing / 2, mount_hole_spacing / 2),
    ])
    .hole(mount_hole_diameter)
)
