import cadquery as cq

outer_radius = 30.0
wall_thickness = 5.0
housing_height = 40.0
rim_chamfer = 2.0
sensor_hole_diameter = 8.0
sensor_hole_depth = 30.0
recess_depth = 8.0
recess_margin = 2.0
rib_width = 4.0
rib_height = 12.0
rib_thickness = wall_thickness
rib_count = 3

outer = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(housing_height)
)

inner_radius = outer_radius - wall_thickness
cavity = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(housing_height - wall_thickness)
)

recess_radius = inner_radius - recess_margin
recess = (
    cq.Workplane("XY")
    .center(0, 0)
    .workplane(offset=housing_height - recess_depth)
    .circle(recess_radius)
    .extrude(recess_depth)
)

result = outer.cut(cavity).cut(recess)

result = (
    result
    .faces(">Z")
    .workplane()
    .hole(sensor_hole_diameter, depth=sensor_hole_depth)
)

angle_step = 360 / rib_count
for i in range(rib_count):
    rib = (
        cq.Workplane("XZ")
        .rect(rib_width, rib_height)
        .extrude(rib_thickness)
        .translate((outer_radius - rib_thickness/2, 0, wall_thickness))
        .rotate((0, 0, 0), (0, 0, 1), i * angle_step)
    )
    result = result.union(rib)

result = result.faces(">Z").edges().chamfer(rim_chamfer)
