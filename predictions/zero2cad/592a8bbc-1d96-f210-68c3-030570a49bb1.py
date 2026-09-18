import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 12.0
bore_diameter = 12.0
keyway_width = 6.0
keyway_depth = 8.0
groove_depth = 5.0
groove_angle = 40.0
chamfer_size = 1.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
bore_radius = bore_diameter / 2.0
half_groove_angle = groove_angle / 2.0
groove_width = 2.0 * groove_depth * math.tan(math.radians(half_groove_angle))

# Base cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
# Central bore
result = result.hole(bore_diameter)
# Keyway cut (rectangular slot in bore)
keyway = (
    cq.Workplane("XY")
    .center(bore_radius - keyway_depth / 2.0, 0)
    .rect(keyway_width, keyway_depth)
    .extrude(thickness)
)
result = result.cut(keyway)
# Chamfer outer edge
result = result.edges("|Z").chamfer(chamfer_size)
# V-groove profile (triangular wedge)
v_profile = (
    cq.Workplane("XY")
    .polyline([
        (outer_radius, 0),
        (outer_radius - groove_depth, groove_width / 2.0),
        (outer_radius - groove_depth, -groove_width / 2.0),
        (outer_radius, 0)
    ])
    .close()
    .extrude(thickness)
)
# Cut first V-groove
result = result.cut(v_profile)
# Cut opposite V-groove rotated 180 degrees
v_profile_opposite = v_profile.rotate((0, 0, 0), (0, 0, 1), 180)
result = result.cut(v_profile_opposite)
