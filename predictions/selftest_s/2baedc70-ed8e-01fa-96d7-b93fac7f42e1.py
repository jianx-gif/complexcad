import cadquery as cq

arm_length = 80.0
step_height = 20.0
base_radius = 15.0
mid_radius = 10.0
tip_radius = 5.0
fillet_radius = 2.0
mount_thickness = 5.0
mount_extra = 5.0
hole_diameter = 4.0
hole_offset = 12.0
boss_width = 30.0
boss_height = 8.0
boss_thickness = 3.0
chamfer_dist = 1.0
vent_dia = 2.0
vent_rows = 3
vent_spacing = 12.0

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, arm_length)
    .lineTo(base_radius, arm_length)
    .lineTo(base_radius, arm_length - step_height)
    .lineTo(mid_radius, arm_length - step_height)
    .lineTo(mid_radius, step_height)
    .lineTo(tip_radius, step_height)
    .lineTo(tip_radius, 0)
    .close()
)

arm = profile.revolve()
arm = arm.translate((0, 0, mount_thickness))
arm = arm.fillet(fillet_radius)

base = (
    cq.Workplane("XY")
    .circle(base_radius + mount_extra)
    .extrude(mount_thickness)
)

result = base.union(arm)
result = result.edges().chamfer(chamfer_dist)

result = (
    result.faces(">Z")
    .workplane()
    .center(hole_offset, 0)
    .hole(hole_diameter)
)

result = (
    result.faces(">Z")
    .workplane()
    .rect(boss_width, boss_height)
    .extrude(boss_thickness)
)

result = (
    result.faces(">Z")
    .workplane(offset=boss_thickness)
    .rarray(vent_spacing, vent_spacing, vent_rows, vent_rows)
    .hole(vent_dia)
)
