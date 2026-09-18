import cadquery as cq

arm_length = 80.0
start_width = 30.0
end_width = 15.0
start_height = 15.0
end_height = 8.0
central_hole_diameter = 8.0
fillet_radius = 0.5
mount_hole_dia = 6.0
mount_spacing = 40.0
mount_offset = 10.0
rib_thickness = 4.0
rib_height = 6.0

start_sketch = cq.Sketch().rect(start_width, start_height)
end_sketch = cq.Sketch().rect(end_width, end_height).moved(cq.Vector(0, 0, arm_length))

arm_body = cq.Workplane().placeSketch(start_sketch, end_sketch).loft()

arm_body = arm_body.edges().fillet(fillet_radius)

through_hole = (
    cq.Workplane("XY")
    .circle(central_hole_diameter / 2)
    .extrude(arm_length + 2)
)

mount_holes = (
    cq.Workplane("XY")
    .pushPoints([(-mount_spacing / 2, mount_offset), (mount_spacing / 2, mount_offset)])
    .circle(mount_hole_dia / 2)
    .extrude(arm_length + 2)
)

arm_body = arm_body.cut(through_hole).cut(mount_holes)

rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_height, centered=False)
    .translate((-start_width / 2, -start_height / 2, 0))
    .extrude(arm_length * 0.25)
)

result = arm_body.union(rib)
