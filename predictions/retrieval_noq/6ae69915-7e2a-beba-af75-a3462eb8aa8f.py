import cadquery as cq

outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
hub_diameter = 30.0
hub_radius = hub_diameter / 2.0
thickness = 5.0
key_slot_width = 8.0
key_slot_length = outer_diameter * 0.6
bolt_hole_diameter = 5.0
bolt_circle_diameter = 20.0
bolt_circle_radius = bolt_circle_diameter / 2.0
chamfer_size = 0.8
rib_width = 6.0
rib_height = 4.0
rib_count = 4
v_groove_depth = 1.5
v_groove_angle = 30.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .rect(key_slot_width, key_slot_length)
    .extrude(thickness)
)

hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .extrude(thickness)
)

pulley = base.union(hub)

v_groove = (
    cq.Workplane("XY")
    .center(outer_radius - v_groove_depth, 0)
    .polygon(3, v_groove_depth * 2)
    .rotate((0, 0, 0), (0, 0, 1), -90)
    .extrude(thickness)
)

pulley = pulley.cut(v_groove)

pulley = (
    pulley
    .faces(">Z")
    .workplane()
    .polarArray(bolt_circle_radius, 0, 360, 4)
    .hole(bolt_hole_diameter)
)

ribs = (
    pulley
    .faces("<Z")
    .workplane()
    .polarArray(outer_radius + rib_height / 2.0, 0, 360, rib_count)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)

pulley = pulley.union(ribs)

pulley = (
    pulley.edges("|Z")
    .chamfer(chamfer_size)
)

result = pulley