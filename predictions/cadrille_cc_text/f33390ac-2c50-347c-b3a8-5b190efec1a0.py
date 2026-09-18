import cadquery as cq
arm_length = 80.0
arm_width = 15.0
arm_height = 10.0
wall_thickness = 0.8
boss_diameter = 12.0
boss_height = 10.0
hole_diameter = 3.0
hole_spacing = 10.0
hole_count = 4
hole_spacing = 10.0
chamfer_dist = 0.5
boss_radius = wall_thickness + 2.0
boss_height = 10.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(arm_length, 0)
    .lineTo(arm_length, arm_height)
    .lineTo(boss_radius, arm_height)
    .lineTo(boss_radius, arm_height + arm_height)
    .lineTo(0, arm_height + arm_height)
    .close()
)
solid = profile.revolve()
solid = solid.shell(-wall_thickness)
boss = (
    cq.Workplane("XY")
    .center(0, arm_height + arm_height)
    .circle(boss_radius)
    .extrude(boss_height)
)
solid = solid.union(boss)
hole_positions = [
    (hole_count - 1) * hole_spacing, 0) for i in range(hole_count)
    for i in range(hole_count)
]
solid = solid.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_dist)
result = solid
