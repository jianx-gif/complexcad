import cadquery as cq
arm_length = 70
arm_thickness = 15
taper_length = 20
boss_radius = 8
boss_height = 25
boss_offset = 12
fillet_radius = 2
chamfer_distance = 1
mount_hole_diameter = 6
arm = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_thickness/2, 0),
        (arm_thickness/2, arm_length - taper_length),
        (0, arm_length)
    ])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
arm = arm.faces("<Y").edges().fillet(fillet_radius)
boss = (
    cq.Workplane("XY")
    .center(boss_offset, boss_height/2)
    .circle(boss_radius)
    .extrude(boss_height)
)
assembly = arm.union(boss)
assembly = assembly.faces("<Y").workplane().hole(mount_hole_diameter)
assembly = assembly.faces(">Z").edges().chamfer(chamfer_distance)
result = assembly