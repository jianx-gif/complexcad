import cadquery as cq

outer_diameter = 60.0
inner_diameter = 30.0
housing_length = 40.0
flange_height = 10.0
flange_extra_radius = 15.0
chamfer_size = 1.5
sensor_pocket_width = 12.0
sensor_pocket_height = 8.0
sensor_pocket_depth = 6.0
sensor_pocket_offset = 20.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
rib_thickness = 2.0
rib_height = 6.0
rib_spacing = 10.0

outer_radius = outer_diameter/2
inner_radius = inner_diameter/2
flange_outer_radius = outer_radius + flange_extra_radius

profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, housing_length)
    .lineTo(flange_outer_radius, housing_length)
    .lineTo(flange_outer_radius, housing_length + flange_height)
    .lineTo(0, housing_length + flange_height)
    .close()
)

result = profile.revolve()

cylinder = cq.Workplane("XY").cylinder(inner_diameter/2, housing_length + flange_height)
result = result.cut(cylinder)

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

result = result.edges("|Z").chamfer(chamfer_size)

result = (
    result
    .faces(">X")
    .workplane()
    .center(sensor_pocket_offset, sensor_pocket_height/2)
    .rect(sensor_pocket_width, sensor_pocket_depth)
    .cutBlind(-sensor_pocket_depth)
)

# Add simple ribs on the flange side for strength
rib = (
    cq.Workplane("XY")
    .lineTo(outer_radius, housing_length)
    .lineTo(outer_radius, housing_length + flange_height)
    .lineTo(outer_radius + rib_thickness, housing_length + flange_height)
    .lineTo(outer_radius + rib_thickness, housing_length)
    .close()
    .revolve()
)

result = result.union(rib)
