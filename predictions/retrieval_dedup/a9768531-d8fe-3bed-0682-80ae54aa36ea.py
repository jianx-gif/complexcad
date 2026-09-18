import cadquery as cq

# Parameters
arm_length = 40.0
outer_root_radius = 6.0
outer_tip_radius = 3.0
taper_length = 10.0
central_hole_diameter = 8.0
mounting_hole_diameter = 4.0
mounting_hole_offset = 12.0
chamfer_distance = 0.5

# Profile for a single arm (XZ plane) using Workplane sketch
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_root_radius, 0)
    .lineTo(outer_root_radius, arm_length - taper_length)
    .spline([
        (outer_root_radius, arm_length - taper_length),
        ((outer_root_radius + outer_tip_radius) / 2, arm_length - taper_length / 2),
        (outer_tip_radius, arm_length)
    ])
    .lineTo(0, arm_length)
    .close()
)

arm = profile.revolve(360)

hole_cyl = (
    cq.Workplane()
    .cylinder(arm_length * 2, mounting_hole_diameter / 2)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((mounting_hole_offset, 0, 0))
)
arm = arm.cut(hole_cyl)

arm90 = arm.rotate((0, 0, 0), (0, 0, 1), 90)
arm180 = arm.rotate((0, 0, 0), (0, 0, 1), 180)
arm270 = arm.rotate((0, 0, 0), (0, 0, 1), 270)
cross = arm.union(arm90).union(arm180).union(arm270)

central_hole = (
    cq.Workplane("XY")
    .circle(central_hole_diameter / 2)
    .extrude(arm_length * 2)
)
cross = cross.cut(central_hole)

cross = cross.edges().chamfer(chamfer_distance)

result = cross