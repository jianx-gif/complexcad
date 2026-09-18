import cadquery as cq

body_diameter = 40.0
body_radius = body_diameter / 2.0
body_length = 60.0
flange_radius = 60.0
flange_thickness = 5.0
central_hole_diameter = 15.0
groove_width = 10.0
groove_depth = 5.0
groove_center = body_length / 2.0
chamfer_distance = 2.0
mount_hole_diameter = 6.0
mount_hole_offset_radius = flange_radius - 10.0
mount_hole_angle = 45.0
rib_height = 2.0
rib_width = 20.0
rib_thickness = 4.0

profile = (
    cq.Sketch()
    .segment((0, 0), (body_radius, 0))
    .segment((body_radius, 0), (body_radius, body_length))
    .segment((body_radius, body_length), (flange_radius, body_length))
    .segment((flange_radius, body_length), (flange_radius, body_length + flange_thickness))
    .segment((flange_radius, body_length + flange_thickness), (0, body_length + flange_thickness))
    .close()
    .assemble()
)

result = (
    cq.Workplane("XY")
    .placeSketch(profile)
    .revolve()
)

result = (
    result
    .workplane(centerOption="CenterOfMass")
    .hole(central_hole_diameter)
)

outer_groove = (
    cq.Workplane("XY")
    .circle(body_radius)
    .extrude(groove_width)
    .translate((0, 0, groove_center - groove_width / 2.0))
)
inner_groove = (
    cq.Workplane("XY")
    .circle(body_radius - groove_depth)
    .extrude(groove_width + 2.0)
    .translate((0, 0, groove_center - groove_width / 2.0 - 1.0))
)
ring_groove = outer_groove.cut(inner_groove)
result = result.cut(ring_groove)

result = (
    result.faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
)

result = (
    result.faces(">Z")
    .workplane(offset=flange_thickness/2.0, centerOption="CenterOfMass")
    .polarArray(mount_hole_offset_radius, 0, mount_hole_angle, 2)
    .hole(mount_hole_diameter)
)

result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
