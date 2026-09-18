import cadquery as cq
from math import cos, sin, pi

outer_diameter = 80.0
gear_length = 50.0
thread_pitch = 8.0
thread_depth = 5.0
bore_diameter_top = 20.0
bore_diameter_bottom = 30.0
sealing_groove_depth = 2.0
hole_diameter = 4.0
hole_count = 6
hole_radius = outer_diameter / 2 - 10.0

outer_radius = outer_diameter / 2.0

base_cyl = cq.Workplane('XY').cylinder(gear_length, outer_radius)

groove_profile = (
    cq.Workplane('XY')
    .center(outer_radius - thread_depth / 2, 0)
    .rect(thread_depth, thread_pitch / 2)
)

revolutions = gear_length / thread_pitch
twist_angle = 360 * revolutions
helical_groove = groove_profile.twistExtrude(gear_length, twist_angle)
gear_body = base_cyl.cut(helical_groove)

bore_cone_solid = cq.Solid.makeCone(gear_length, bore_diameter_top / 2, bore_diameter_bottom / 2)
bore_cone = cq.Workplane('XY').add(bore_cone_solid).translate((0, 0, -gear_length / 2)).val()
gear_with_bore = gear_body.cut(bore_cone)

sealing_groove = (
    cq.Workplane('XY')
    .cylinder(sealing_groove_depth, outer_radius - sealing_groove_depth)
    .translate((0, 0, gear_length / 2 - sealing_groove_depth / 2))
)
gear_with_groove = gear_with_bore.cut(sealing_groove)

points = [
    (hole_radius * cos(i * 2 * pi / hole_count), hole_radius * sin(i * 2 * pi / hole_count))
    for i in range(hole_count)
]
result = (
    gear_with_groove
    .faces('>Z')
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)
