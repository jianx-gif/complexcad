import cadquery as cq
import math

module = 2.0
num_teeth = 44
pressure_angle = 20.0
face_width = 20.0
helix_angle = 15.0
key_width = 6.0
key_height = 12.0
key_depth = 6.0
chamfer_size = 0.8
shaft_diameter = 10.0
mount_hole_diameter = 4.0
mount_hole_radius = 30.0

addendum = module
dedendum = 1.25 * module
pitch_diameter = num_teeth * module
base_radius = pitch_diameter / 2.0
outer_radius = base_radius + addendum
root_radius = base_radius - dedendum

points = []
for i in range(num_teeth * 2):
    angle_deg = i * (360.0 / (num_teeth * 2))
    angle_rad = math.radians(angle_deg)
    radius = outer_radius if i % 2 == 0 else root_radius
    x = radius * math.cos(angle_rad)
    y = radius * math.sin(angle_rad)
    points.append((x, y))

gear_profile = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
)

twist_angle = 360.0 * math.tan(math.radians(helix_angle))

gear_body = (
    gear_profile
    .twistExtrude(face_width, twist_angle)
)

gear_body = (
    gear_body
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .hole(shaft_diameter)
)

gear_body = (
    gear_body
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .polarArray(mount_hole_radius, 0, 120, 3)
    .hole(mount_hole_diameter)
)

gear_body = (
    gear_body
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .rect(key_width, key_height)
    .cutBlind(-key_depth)
)

result = (
    gear_body
    .faces(">Z")
    .edges()
    .first()
    .chamfer(chamfer_size)
)
