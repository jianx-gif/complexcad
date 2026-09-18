import cadquery as cq

# Parameters
cap_outer_radius = 40.0
cap_height = 30.0
wall_thickness = 3.0
boss_radius = 10.0
boss_height = 12.0
vent_hole_radius = 4.0
vent_hole_count = 3
vent_hole_angle = 360.0 / vent_hole_count
fillet_radius = 1.2
chamfer_distance = 0.8
seal_groove_depth = 1.5
seal_groove_width = 2.0

# Base profile and revolve
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(cap_outer_radius, 0)
    .lineTo(cap_outer_radius, cap_height - boss_height)
    .lineTo(boss_radius, cap_height - boss_height)
    .lineTo(boss_radius, cap_height)
    .lineTo(0, cap_height)
    .close()
)
result = profile.revolve()
# Chamfer outer bottom edge for deburring
result = result.edges().chamfer(chamfer_distance)
# Fillet remaining edges for safety
result = result.edges().fillet(fillet_radius)
# Seal groove (internal pocket near top of boss)
groove = (
    cq.Workplane("XY")
    .center(0, cap_height - seal_groove_depth / 2)
    .circle(boss_radius - wall_thickness / 2)
    .extrude(seal_groove_depth)
)
result = result.cut(groove)
# Vent holes (radial cuts equally spaced)
vent_z = cap_height / 2.0
vent_cylinder = (
    cq.Workplane("XZ")
    .center(cap_outer_radius - wall_thickness / 2.0, vent_z)
    .circle(vent_hole_radius)
    .extrude(wall_thickness + 2.0, both=True)
)
for i in range(vent_hole_count):
    angle = i * vent_hole_angle
    rotated = vent_cylinder.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated)
