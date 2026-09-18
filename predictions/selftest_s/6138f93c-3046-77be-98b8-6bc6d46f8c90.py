import cadquery as cq

plate_width = 80.0
plate_length = 60.0
cylinder_base_radius = 30.0
cylinder_height = 50.0
loft_steps = 4
chamfer_size = 1.0
bolt_diameter = 5.0
counterbore_diameter = 9.0
counterbore_depth = 4.0
rib_width = 5.0
rib_height = 20.0
rib_thickness = 3.0

step_height = cylinder_height / (loft_steps + 1)
target_radius = plate_width / 2.0
radius_increment = (target_radius - cylinder_base_radius) / (loft_steps + 1)

result = (
    cq.Workplane("XY")
    .circle(cylinder_base_radius)
)
for i in range(1, loft_steps + 1):
    radius = cylinder_base_radius + i * radius_increment
    offset = i * step_height
    result = result.workplane(offset=offset).circle(radius)
result = (
    result
    .workplane(offset=cylinder_height)
    .rect(plate_width, plate_length)
    .loft(combine=True)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .cboreHole(bolt_diameter, counterbore_diameter, counterbore_depth)
)
result = (
    result
    .faces("<X")
    .workplane()
    .rect(rib_thickness, rib_height)
    .extrude(rib_width)
)
result = result.edges(">Z").chamfer(chamfer_size)
