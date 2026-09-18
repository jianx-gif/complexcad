import cadquery as cq

outer_diameter = 70
inner_diameter = 45
housing_length = 60
bevel_chamfer = 3
sensor_pocket_width = 30
sensor_pocket_height = 20
sensor_pocket_depth = 10
mount_hole_dia = 5
mount_hole_spacing = 40
rib_height = 5
rib_inset = 10

result = cq.Workplane("XY").circle(outer_diameter / 2).extrude(housing_length)
result = result.faces(">Z").edges().chamfer(bevel_chamfer)
result = result.faces(">Z").workplane().hole(inner_diameter)
result = result.faces(">Y").first().workplane().center(0, 0).rect(sensor_pocket_width, sensor_pocket_height).cutBlind(-sensor_pocket_depth)
result = result.faces(">Z").workplane().pushPoints([(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)]).hole(mount_hole_dia)
result = result.faces(">Z").workplane().center(0, 0).rect(outer_diameter - 2 * rib_inset, sensor_pocket_width).extrude(-rib_height)
