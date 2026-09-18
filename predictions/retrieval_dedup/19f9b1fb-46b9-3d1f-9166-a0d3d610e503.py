import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 40.0
thickness = 15.0
key_width = 10.0
key_depth = 8.0
key_angle = 30.0
chamfer_dist = 2.0
mount_hole_diameter = 6.0
relief_width = 12.0
relief_depth = 5.0
rib_height = 3.0
rib_width = 6.0
rib_spacing_deg = 30.0

result = cq.Workplane("XY").circle(outer_diameter/2).extrude(thickness)
result = result.faces(">Z").workplane().hole(inner_diameter)

keybox = cq.Workplane("XY").box(key_depth, key_width, thickness)
keybox = keybox.translate((inner_diameter/2 + key_depth/2, 0, 0)).rotate((0,0,0), (0,0,1), key_angle)
result = result.cut(keybox)

hole_radius = outer_diameter/2 - 5.0
p1 = (hole_radius*math.cos(math.radians(0)), hole_radius*math.sin(math.radians(0)))
p2 = (hole_radius*math.cos(math.radians(180)), hole_radius*math.sin(math.radians(180)))
result = result.faces(">Z").workplane().pushPoints([p1, p2]).hole(mount_hole_diameter)

result = result.faces(">Z").workplane().pushPoints([p1, p2]).rect(relief_width, relief_width).cutBlind(-relief_depth)

num_ribs = int(360 / rib_spacing_deg)
for i in range(num_ribs):
    angle = i * rib_spacing_deg
    rib = cq.Workplane("XY").box(rib_height, rib_width, thickness)
    rib = rib.translate((inner_diameter/2 + rib_height/2, 0, 0)).rotate((0,0,0), (0,0,1), angle)
    result = result.union(rib)

result = result.edges(">Z").chamfer(chamfer_dist)
